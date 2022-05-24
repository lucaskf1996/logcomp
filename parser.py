from ast import (Node, BinOp, UnOp, IntVal, StrVal, IdOp, NoOp, Block, PrintOp, AssignOp, WhileOp, IfOp, VarDec, ScanOp)
from st import SymbolTable
from tokens import (Token, Tokenizer)
import re
from writer import Writer

class Parser:

    tokens = None

    def Factor():
        # print(Parser.tokens.actual.tokenType)
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
            node = IdOp(Parser.tokens.actual.tokenValue)
            # print("identifier")
            Parser.tokens.selectNext()
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
        # print("lol" + Parser.tokens.actual.tokenType)
        if(Parser.tokens.actual.tokenType == "OBLOCK"):
            Parser.tokens.selectNext()
            while(Parser.tokens.actual.tokenType != "CBLOCK"):
                # node.__repr__()
                if(Parser.tokens.actual.tokenType == "EOF"):
                    raise Exception("Block not closed")
                node.addChild(Parser.parseStatement())
                # print("teste"+Parser.tokens.actual.tokenType)
                # print("teste"+Parser.tokens.actual.tokenType)
                # node.__repr__()
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
            node = IdOp(Parser.tokens.actual.tokenValue)
            Parser.tokens.selectNext()
            # print(Parser.tokens.actual.tokenType)
            if(Parser.tokens.actual.tokenType == "EQUAL"):
                node = AssignOp([node, Parser.parseRelationalExpression()], "=")
                if(Parser.tokens.actual.tokenType == "SC"):
                    Parser.tokens.selectNext()
                    # print("teste"+Parser.tokens.actual.tokenType)
                else:
                    # print(Parser.tokens.actual.tokenType)
                    raise Exception("missing semi colon")
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
        Parser.tokens = Tokenizer(Parser.code_cleanup(code))
        Parser.tokens.selectNext()
        Parser.writer = Writer()
        root = Parser.parseBlock()
        if(Parser.tokens.actual.tokenType == "EOF"):
            root.Evaluate(Parser.symbolTable, Parser.writer)
            Parser.writer.end()
            
        else:
            raise Exception("invalid sequence")