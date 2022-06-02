from ast import (Node, BinOp, UnOp, IntVal, StrVal, IdOp, NoOp, Block, PrintOp, AssignOp, WhileOp, IfOp, VarDec, ScanOp, Program, FuncDec, FuncCall, ReturnOp)
from st import SymbolTable
from ft import FunctionTable
from tokens import (Token, Tokenizer)
import re

class Parser:

    tokens = None

    def parseProgram():
        # Parser.tokens.selectNext()
        node = Program()
        while(Parser.tokens.actual.tokenType != "EOF"):
            # print(Parser.tokens.actual.tokenType)
            node.addChild(Parser.parseDeclaration())
        node.addChild(FuncCall("main", []))
        return node

    def parseDeclaration():
        # print(Parser.tokens.actual.tokenType)
        # Parser.tokens.selectNext()
        if(Parser.tokens.actual.tokenType == "TYPE"):
            declType = Parser.tokens.actual.tokenValue
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.tokenType == "ID"):
                declId = Parser.tokens.actual.tokenValue
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.tokenType == "OP"):
                    Parser.tokens.selectNext()
                    args = []
                    if(Parser.tokens.actual.tokenType != "CP"):
                        if(Parser.tokens.actual.tokenType == "TYPE"):
                            child = VarDec(Parser.tokens.actual.tokenValue)
                            Parser.tokens.selectNext()
                            if(Parser.tokens.actual.tokenType == "ID"):
                                child.addChild(IdOp(Parser.tokens.actual.tokenValue))
                                # child.__repr__()
                                Parser.tokens.selectNext()
                                args.append(child)
                                while(Parser.tokens.actual.tokenType == "COMMA"):
                                    Parser.tokens.selectNext()
                                    if(Parser.tokens.actual.tokenType == "TYPE"):
                                        child = VarDec(Parser.tokens.actual.tokenValue)
                                        Parser.tokens.selectNext()
                                        if(Parser.tokens.actual.tokenType == "ID"):
                                            child.addChild(IdOp(Parser.tokens.actual.tokenValue))
                                            args.append(child)
                                            # child.__repr__()
                                            Parser.tokens.selectNext()
                                        else:
                                            raise Exception("invalid sequence")
                                    else:
                                        raise Exception("invalid sequence")
                                if(Parser.tokens.actual.tokenType == "CP"):
                                    Parser.tokens.selectNext()
                                    # print(Parser.tokens.actual.tokenType)
                                    # print(declId, declType)
                                    node = FuncDec([declId, declType], args, Parser.parseBlock())
                                    return node
                                else:
                                    raise Exception("invalid sequence")
                            else:
                                raise Exception("invalid sequence")
                    elif(Parser.tokens.actual.tokenType == "CP"):
                        Parser.tokens.selectNext()
                        node = FuncDec([declId,declType], args, Parser.parseBlock())
                        return node
                    else:
                        raise Exception("invalid sequence")
                else:
                    raise Exception("invalid sequence")
            else:
                raise Exception("invalid sequence")
        else:
            raise Exception("invalid sequence")
        raise Exception("invalid sequence")

    def Factor():
        # print(Parser.tokens.actual.tokenType)
        # print(f"{Parser.tokens.actual.tokenValue}   {Parser.tokens.actual.tokenType}")
        Parser.tokens.selectNext()
        # print("Factor"+Parser.tokens.actual.tokenType)
        if(Parser.tokens.actual.tokenType == "NUM"):
            node = IntVal(Parser.tokens.actual.tokenValue)
            # print("numero")
            Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "STR"):
            node = StrVal(Parser.tokens.actual.tokenValue)
            Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "ID"):
            # print("teste  ", Parser.tokens.actual.tokenType)
            id = Parser.tokens.actual.tokenValue
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.tokenType == "OP"):
                Parser.tokens.smallLook()
                args = []
                if(Parser.tokens.actual.tokenType != "CP"):
                    while(Parser.tokens.actual.tokenType != "CP"):
                        child = Parser.parseRelationalExpression()
                        # print(type(child))
                        args.append(child)
                        if(Parser.tokens.actual.tokenType == "COMMA"):
                            child = Parser.parseRelationalExpression()
                            # print(type(child))
                            args.append(child)
                            if(Parser.tokens.actual.tokenType == "CP"):
                                node = FuncCall(id, args)
                            else:
                                raise Exception("invalid sequence")
                        else:
                            raise Exception("invalid sequence")
                    Parser.tokens.selectNext()
                elif(Parser.tokens.actual.tokenType == "CP"):
                    node = FuncCall(id, [])
                    Parser.tokens.selectNext()
                    # print("teste25  ", Parser.tokens.actual.tokenType)
                else:
                    raise Exception("invalid sequence")
            else:
                # print("teste  ", Parser.tokens.actual.tokenType)
                node = IdOp(id)
        elif(Parser.tokens.actual.tokenType == "MINUS"):
            node = UnOp(Parser.tokens.actual.tokenType, Parser.Factor())
            # Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "PLUS"):
            node = UnOp(Parser.tokens.actual.tokenType, Parser.Factor())
            # Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "NOT"):
            node = UnOp(Parser.tokens.actual.tokenType, Parser.Factor())
            # Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "SCANF"):
            node = ScanOp()
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.tokenType == "OP"):
                Parser.tokens.selectNext()
                # print(Parser.tokens.actual.tokenType)
                if(Parser.tokens.actual.tokenType == "CP"):
                    Parser.tokens.selectNext()
                    return node
                else:
                    raise Exception("invalid sequence1")   
            else:
                raise Exception("invalid sequence")
        elif(Parser.tokens.actual.tokenType == "OP"):
            node = Parser.parseRelationalExpression()
            if(Parser.tokens.actual.tokenType == "CP"):
                Parser.tokens.selectNext()
                return node
            else:
                raise Exception("invalid sequence")
        else:
            # print(Parser.tokens.actual.tokenType)
            raise Exception("invalid sequence2")
            
        return node

    def parseTerm():
        node = Parser.Factor()
        # print("Term"+Parser.tokens.actual.tokenType)
        while(Parser.tokens.actual.tokenType == "MULT" or Parser.tokens.actual.tokenType == "DIV" or Parser.tokens.actual.tokenType == "AND"):
            if(Parser.tokens.actual.tokenType == "MULT"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.Factor()])
            elif(Parser.tokens.actual.tokenType == "DIV"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.Factor()])
            elif(Parser.tokens.actual.tokenType == "AND"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.Factor()])
        return node

    def parseExpression():
        node = Parser.parseTerm()
        # print("Expression"+Parser.tokens.actual.tokenType)
        while(Parser.tokens.actual.tokenType == "PLUS" or Parser.tokens.actual.tokenType == "MINUS" or Parser.tokens.actual.tokenType == "OR" or Parser.tokens.actual.tokenType == "CONCAT"):
            if(Parser.tokens.actual.tokenType == "PLUS"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.parseTerm()])
            elif(Parser.tokens.actual.tokenType == "MINUS"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.parseTerm()])
            elif(Parser.tokens.actual.tokenType == "OR"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.parseTerm()])
            elif(Parser.tokens.actual.tokenType == "CONCAT"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.parseTerm()])
            
        return node

    def parseRelationalExpression():
        node = Parser.parseExpression()
        # node.__repr__()
        # print("RelExp"+Parser.tokens.actual.tokenType)
        while(Parser.tokens.actual.tokenType == "BOOLEQUAL" or Parser.tokens.actual.tokenType == "LESS" or Parser.tokens.actual.tokenType == "MORE"):
            if(Parser.tokens.actual.tokenType == "BOOLEQUAL"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.parseExpression()])
            elif(Parser.tokens.actual.tokenType == "LESS"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.parseExpression()])
            elif(Parser.tokens.actual.tokenType == "MORE"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.parseExpression()])
        return node

    def parseBlock():
        node = Block()
        if(Parser.tokens.actual.tokenType == "OBLOCK"):
            Parser.tokens.selectNext()
            while(Parser.tokens.actual.tokenType != "CBLOCK"):
                if(Parser.tokens.actual.tokenType == "EOF"):
                    raise Exception("Block not closed")
                node.addChild(Parser.parseStatement())
            Parser.tokens.selectNext()
        else:
            raise Exception("Block not opened")
        return node

    def parseStatement():
        # Parser.tokens.selectNext()
        # print("Statement" + Parser.tokens.actual.tokenType)
        if(Parser.tokens.actual.tokenType == "SC"):
            node = NoOp()
            Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "TYPE"):
            node = VarDec(Parser.tokens.actual.tokenValue)
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.tokenType == "ID"):
                node.addChild(IdOp(Parser.tokens.actual.tokenValue))
                Parser.tokens.selectNext()
                while(Parser.tokens.actual.tokenType!="SC"):
                    if(Parser.tokens.actual.tokenType == "COMMA"):
                        Parser.tokens.selectNext()
                        if(Parser.tokens.actual.tokenType == "ID"):
                            node.addChild(IdOp(Parser.tokens.actual.tokenValue))

                            Parser.tokens.selectNext()
                        else:
                            raise Exception("not a valid variable")
                    else:
                        raise Exception("not a valid variable")
                Parser.tokens.selectNext()
            else:
                raise Exception("not a valid variable")
        elif(Parser.tokens.actual.tokenType == "ID"):
            id = Parser.tokens.actual.tokenValue
            Parser.tokens.selectNext()
            # print(Parser.tokens.actual.tokenType)
            if(Parser.tokens.actual.tokenType == "EQUAL"):
                # print(id)
                node = IdOp(id)
                node = AssignOp([node, Parser.parseRelationalExpression()], "=")
                if(Parser.tokens.actual.tokenType == "SC"):
                    Parser.tokens.selectNext()
                    # print("teste"+Parser.tokens.actual.tokenType)
                else:
                    # print(Parser.tokens.actual.tokenType)
                    raise Exception("missing semi colon")
            elif(Parser.tokens.actual.tokenType == "OP"):
                Parser.tokens.smallLook()
                args = []
                if(Parser.tokens.actual.tokenType != "CP"):
                    while(Parser.tokens.actual.tokenType != "CP"):
                        args.append(Parser.parseRelationalExpression())
                        if(Parser.tokens.actual.tokenType == "COMMA"):
                            args.append(Parser.parseRelationalExpression())
                            if(Parser.tokens.actual.tokenType == "CP"):
                                node = FuncCall(id, args)
                            else:
                                raise Exception("invalid sequence")
                        else:
                            raise Exception("invalid sequence")
                    Parser.tokens.selectNext()
                elif(Parser.tokens.actual.tokenType == "CP"):
                    node = FuncCall(id, [])
                    Parser.tokens.selectNext()
                else:
                    raise Exception("invalid sequence")
            else:
                raise Exception("invalid sequence")
        elif(Parser.tokens.actual.tokenType == "RETURN"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.tokenType == "OP"):
                # Parser.tokens.selectNext()
                node = ReturnOp("return", Parser.parseRelationalExpression())
                if(Parser.tokens.actual.tokenType == "CP"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.tokenType == "SC"):
                        Parser.tokens.selectNext()
                    else:
                        raise Exception("invalid sequence")
                else:
                    raise Exception("invalid sequence")
            else:
                raise Exception("invalid sequence")
        elif(Parser.tokens.actual.tokenType == "PRINTF"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.tokenType == "OP"):
                node = PrintOp(Parser.parseRelationalExpression())
                if(Parser.tokens.actual.tokenType == "CP"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.tokenType == "SC"):
                        Parser.tokens.selectNext()
                    else:
                        raise Exception("missing semi colon")
                else:
                    raise Exception("missing parenthesis")
            else:
                raise Exception("missing parenthesis")
        elif(Parser.tokens.actual.tokenType == "WHILE"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.tokenType == "OP"):
                child1 = Parser.parseRelationalExpression()
                # Parser.tokens.selectNext()
                if(Parser.tokens.actual.tokenType == "CP"):
                    Parser.tokens.selectNext()
                    # print("kek" + Parser.tokens.actual.tokenType)
                    node = WhileOp([child1, Parser.parseStatement()])
                    # node.__repr__()
                    # Parser.tokens.selectNext()
                else:
                    raise Exception("missing parenthesis")
            else:
                raise Exception("missing parenthesis")
        elif(Parser.tokens.actual.tokenType == "IF"):
            Parser.tokens.selectNext()
            # print("kek" + Parser.tokens.actual.tokenType)
            if(Parser.tokens.actual.tokenType == "OP"):
                child1 = Parser.parseRelationalExpression()
                # print("kek" + Parser.tokens.actual.tokenType)
                if(Parser.tokens.actual.tokenType == "CP"):
                    Parser.tokens.selectNext()
                    child2 = Parser.parseStatement()
                    child3 = NoOp()
                    # Parser.tokens.selectNext()
                    if(Parser.tokens.actual.tokenType == "ELSE"):
                        Parser.tokens.selectNext()
                        child3 = Parser.parseStatement()
                        # print("teste" + Parser.tokens.actual.tokenType)
                    node = IfOp([child1, child2, child3])
                else:
                    raise Exception("missing parenthesis")
            else:
                raise Exception("missing parenthesis")
        elif(Parser.tokens.actual.tokenType == "OBLOCK"):
            # print("lol"+Parser.tokens.actual.tokenType)
            # Parser.tokens.selectNext()
            node = Parser.parseBlock()
        else:
            raise Exception("invalid sequence")

        return node

    def code_cleanup1(code):
        return(re.sub(r'/[*](.*?)[*]/',"", code))

    def code_cleanup(text): # FROM https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " " # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        return re.sub(pattern, replacer, text)
                    
    def run(code):
        Parser.symbolTable = SymbolTable()
        Parser.functionTable = FunctionTable()
        Parser.tokens = Tokenizer(Parser.code_cleanup(code))
        Parser.tokens.selectNext()
        root = Parser.parseProgram()
        if(Parser.tokens.actual.tokenType == "EOF"):
            root.Evaluate(Parser.symbolTable, Parser.functionTable)
        else:
            raise Exception("invalid sequence")