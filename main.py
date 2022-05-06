import sys
import re

class Node():
    def Evaluate(self, symbolTable):
        pass

class BinOp(Node):
    def __init__(self, value, nodes):
        self.value = value
        self.children = nodes

    def __repr__(self):
        print(self.value, " children ->( ")
        self.children[0].__repr__()
        self.children[1].__repr__()
        print(" ) ")

    def Evaluate(self, symbolTable):
        child1 = self.children[0].Evaluate(symbolTable)
        child2 = self.children[1].Evaluate(symbolTable)
        # print(child1, child2)
        if self.value == "PLUS":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] + child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "MINUS":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] - child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "MULT":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] * child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "DIV":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] // child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "BOOLEQUAL":
            # print(type(self.children[0]), type(self.children[1]))
            if(child1[1] == child2[1]):
                if(child1[0] == child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "LESS":
            if(child1[1] == child2[1]):
                if(child1[0] < child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "MORE":
            if(child1[1] == child2[1]):
                if(child1[0] > child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "OR":
            if(child1[1] == child2[1]):
                if(child1[0] or child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "AND":
            if(child1[1] == child2[1]):
                if(child1[0] and child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "CONCAT":
            return (str(child1[0]) + str(child2[0]), "str")
        else:
            raise Exception("Evaluate Error")

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def __repr__(self):
        print(self.value, " child -> ( ")
        self.children.__repr__()
        print(" ) ")

    def Evaluate(self, symbolTable):
        child = self.children.Evaluate(symbolTable)
        if child[1] != "int":
            raise Exception("cannot make operation with str")
        if self.value == "PLUS":
            return (child[0], "int")
        elif self.value == "MINUS":
            return (-child[0], "int")
        elif self.value == "NOT":
            return (not child[0], "int")
        else:
            raise Exception("Evaluate Error")

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print(int(self.value), " ")

    def Evaluate(self, symbolTable):
        if self.value.isnumeric():
            return (int(self.value), "int")
        else:
            raise Exception("Evaluate Error")

class StrVal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print(self.value, " ")

    def Evaluate(self, symbolTable):
        return (self.value, "str")

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = None

    def __repr__(self):
        print("No Children")

    def Evaluate(self, symbolTable):
        return

class IdOp(Node):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        print(self.value, " ")
    
    def Evaluate(self, symbolTable):
        return symbolTable.getValue(self.value) #ja retorna como tupla

class Block(Node):
    def __init__(self):
        self.children = []

    def __repr__(self):
        print("Block children -> ( ")
        for child in self.children:
            child.__repr__()
        print(" ) ")

    def addChild(self, child):
        self.children.append(child)

    def Evaluate(self, symbolTable):
        for child in self.children:
            child.Evaluate(symbolTable)

class PrintOp(Node):
    def __init__(self, child):
        self.child = child
    
    def __repr__(self):
        print("PRINTF", " child -> ( ")
        self.child.__repr__()
        print(" ) ")

    def Evaluate(self, symbolTable):
        child = self.child.Evaluate(symbolTable)[0]
        print(child)

class AssignOp(Node):
    def __init__(self, children, value):
        self.children = children
        self.value = value

    def __repr__(self):
        print(self.value, " children ->( ")
        self.children[0].__repr__()
        self.children[1].__repr__()
        print(" ) ")

    def Evaluate(self, symbolTable):
        symbolTable.setValue(self.children[0].value, self.children[1].Evaluate(symbolTable))
        return

class WhileOp(Node):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        print("WHILE children ->( ")
        self.children[0].__repr__()
        self.children[1].__repr__()
        print(" ) ")
    
    def Evaluate(self, symbolTable):
        while(self.children[0].Evaluate(symbolTable)[0]):
            # self.children[1].__repr__()
            self.children[1].Evaluate(symbolTable)
        return

class IfOp(Node):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        print("IF children ->( ")
        self.children[0].__repr__()
        self.children[1].__repr__()
        if(self.children[2] != None):
            self.children[2].__repr__()
        print(" ) ")
    
    def Evaluate(self, symbolTable):
        if(self.children[0].Evaluate(symbolTable)[0]):
            self.children[1].Evaluate(symbolTable)
        else:
            self.children[2].Evaluate(symbolTable)
        return

class VarDec(Node):

    def __init__(self, value):
        self.children = []
        self.value = value

    def __repr__(self):
        print("VarDec children -> ( ")
        for child in self.children:
            child.__repr__()
        print(" ) ")

    def addChild(self, child):
        self.children.append(child)

    def Evaluate(self, symbolTable):
        for i in self.children:
            symbolTable.create(i.value, self.value)

class ScanOp(Node):

    def __repr__(self):
        print("SCAN")
    
    def Evaluate(self, symbolTable):
        try:
            inp = int(input())
        except:
            raise Exception("not a int")
        return (inp, "int")

class Token:
    def __init__(self, tokenType, tokenValue):
        self.tokenType = tokenType 
        self.tokenValue = tokenValue 

class Tokenizer:

    def __init__(self, origin):
        self.origin = origin 
        self.position = 0
        self.actual = Token(None, None) 

    def selectNext(self):
        printteste = 0
        num=None
        while(len(self.origin)>self.position):
            if(self.origin[self.position] == "\n"):
                self.position+=1
                continue
            elif(self.origin[self.position].isalpha()):
                alpha = self.origin[self.position]
                self.position+=1
                while(self.position != len(self.origin)):
                    if(self.origin[self.position].isnumeric() or self.origin[self.position].isalpha() or self.origin[self.position] == "_"):
                        alpha = alpha + self.origin[self.position]
                        self.position+=1
                    else:
                        if(alpha == "printf"):
                            self.actual = Token("PRINTF", 0)
                            if(printteste): print(self.actual.tokenType)
                            return
                        elif(alpha == "scanf"):
                            self.actual = Token("SCANF", 0)
                            if(printteste): print(self.actual.tokenType)
                            return
                        elif(alpha == "while"):
                            self.actual = Token("WHILE", 0)
                            if(printteste): print(self.actual.tokenType)
                            return
                        elif(alpha == "if"):
                            self.actual = Token("IF", 0)
                            if(printteste): print(self.actual.tokenType)
                            return
                        elif(alpha == "else"):
                            self.actual = Token("ELSE", 0)
                            if(printteste): print(self.actual.tokenType)
                            return
                        elif(alpha == "int"):
                            self.actual = Token("TYPE", 0)
                            if(printteste): print(self.actual.tokenType)
                            return
                        elif(alpha == "str"):
                            self.actual = Token("TYPE", 1)
                            if(printteste): print(self.actual.tokenType)
                            return
                        self.actual = Token("ID", alpha)
                        if(printteste): print(self.actual.tokenType)
                        return
            elif(self.origin[self.position].isnumeric()):
                num = self.origin[self.position]
                self.position+=1
                while(self.position != len(self.origin)):
                    if(self.origin[self.position].isnumeric()):
                        num = num + self.origin[self.position]
                        self.position+=1
                    elif(self.origin[self.position].isalpha() or self.origin[self.position] == "_"):
                        raise Exception("invalid number")
                    else:
                        self.actual = Token("NUM", num)
                        if(printteste): print(self.actual.tokenType)
                        return
                self.actual = Token("NUM", num)
                if(printteste): print(self.actual.tokenType)
                return
            elif(self.origin[self.position] == "\""):
                self.position+=1
                string = ""
                while(self.origin[self.position] != "\""):
                    string+=self.origin[self.position]
                    self.position+=1
                self.actual = Token("STR", string)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == ","):
                self.actual = Token("COMMA", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "+"):
                self.actual = Token("PLUS", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "-"):
                self.actual = Token("MINUS", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "*"):
                self.actual = Token("MULT", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "/"):
                self.actual = Token("DIV", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "("):
                self.actual = Token("OP", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == ")"):
                self.actual = Token("CP", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "{"):
                self.actual = Token("OBLOCK", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "}"):
                self.actual = Token("CBLOCK", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == ";"):
                self.actual = Token("SC", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "="):
                if(self.origin[self.position+1] == "="):
                    self.actual = Token("BOOLEQUAL", 0)
                    if(printteste): print(self.actual.tokenType)
                    self.position+=2
                    return
                else:
                    self.actual = Token("EQUAL", 0)
                    if(printteste): print(self.actual.tokenType)
                    self.position+=1
                    return
            elif(self.origin[self.position] == "<"):
                self.actual = Token("LESS", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == ">"):
                self.actual = Token("MORE", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "&"):
                if(self.origin[self.position+1] == "&"):
                    self.actual = Token("AND", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=2
                return
            elif(self.origin[self.position] == "|"):
                if(self.origin[self.position+1] == "|"):
                    self.actual = Token("OR", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=2
                return
            elif(self.origin[self.position] == "!"):
                self.actual = Token("NOT", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == "."):
                self.actual = Token("CONCAT", 0)
                if(printteste): print(self.actual.tokenType)
                self.position+=1
                return
            elif(self.origin[self.position] == " "):
                self.position+=1
                continue
            elif(self.origin[self.position] == "\n"):
                self.position+=1
                continue
            else:
                # print(self.origin[self.position])
                raise Exception("Invalid char")
        self.actual = Token("EOF", 0)
        return
        
class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def getValue(self, identifier):
        try:
            return tuple(self.table[identifier])
        except:
            raise Exception("variable is not declared")
    
    def setValue(self, identifier, value):
        print(value)
        if(identifier in self.table.keys()):
            if(self.table[identifier][1] == "int" and value[1] == "int"):
                self.table[identifier][0] = value[0]
            else:
                if(value[1] == "str"):
                    self.table[identifier][0] = value
                else:
                    raise Exception("cannot add an int to a str variable")
        else:
            raise Exception("variable is not declared")

    def create(self, identifier, value):
        if(identifier in self.table.keys()):
            raise Exception("variable cannot be redeclared")
        if(value == 0):
            self.table[identifier] = [None, "int"]
        elif(value == 1):
            self.table[identifier] = [None, "str"]

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
        root = Parser.parseBlock()
        # Parser.tokens.selectNext()
        # root.__repr__()
        if(Parser.tokens.actual.tokenType == "EOF"):
            return root.Evaluate(Parser.symbolTable)
        else:
            raise Exception("invalid sequence")

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
    Parser.run(contents)
    # print(Parser.run(sys.argv[1]))