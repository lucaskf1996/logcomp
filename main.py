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
        if self.value == "PLUS":
            return self.children[0].Evaluate(symbolTable) + self.children[1].Evaluate(symbolTable)
        elif self.value == "MINUS":
            return self.children[0].Evaluate(symbolTable) - self.children[1].Evaluate(symbolTable)
        elif self.value == "MULT":
            return self.children[0].Evaluate(symbolTable) * self.children[1].Evaluate(symbolTable)
        elif self.value == "DIV":
            return self.children[0].Evaluate(symbolTable) // self.children[1].Evaluate(symbolTable)
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
        if self.value == "PLUS":
            return self.children.Evaluate(symbolTable)
        elif self.value == "MINUS":
            return -self.children.Evaluate(symbolTable)
        else:
            raise Exception("Evaluate Error")

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print(int(self.value), " ")

    def Evaluate(self, symbolTable):
        if self.value.isnumeric():
            return int(self.value)
        else:
            raise Exception("Evaluate Error")

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
        return symbolTable.getValue(self.value)

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
        print(self.child.Evaluate(symbolTable))

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
                            return
                        self.actual = Token("ID", alpha)
                        return
            elif(self.origin[self.position].isnumeric()):
                num = self.origin[self.position]
                self.position+=1
                while(self.position != len(self.origin)):
                    if(self.origin[self.position].isnumeric()):
                        num = num + self.origin[self.position]
                        self.position+=1
                    else:
                        self.actual = Token("NUM", num)
                        return
                self.actual = Token("NUM", num)
                return
            elif(self.origin[self.position] == "+"):
                self.actual = Token("PLUS", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "-"):
                self.actual = Token("MINUS", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "*"):
                self.actual = Token("MULT", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "/"):
                self.actual = Token("DIV", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "("):
                self.actual = Token("OP", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == ")"):
                self.actual = Token("CP", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "{"):
                self.actual = Token("OBLOCK", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "}"):
                self.actual = Token("CBLOCK", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "="):
                self.actual = Token("EQUAL", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == ";"):
                self.actual = Token("SC", 0)
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
            return self.table[identifier]
        except:
            raise Exception("variable is not found")
    
    def setValue(self, identifier, value):
        # try:
        self.table[identifier] = value
        # except:
        #     raise Exception("variable is not found")

class Parser:

    tokens = None

    def Factor():
        Parser.tokens.selectNext()
        if(Parser.tokens.actual.tokenType == "NUM"):
            node = IntVal(Parser.tokens.actual.tokenValue)
            Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "ID"):
            node = IdOp(Parser.tokens.actual.tokenValue)
            Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "MINUS"):
            node = UnOp(Parser.tokens.actual.tokenType, Parser.Factor())
        elif(Parser.tokens.actual.tokenType == "PLUS"):
            node = UnOp(Parser.tokens.actual.tokenType, Parser.Factor())
        elif(Parser.tokens.actual.tokenType == "OP"):
            node = Parser.parseExpression()
            if(Parser.tokens.actual.tokenType == "CP"):
                Parser.tokens.selectNext()
                return node
            else:
                raise Exception("invalid sequence2.1")
        else:
            # print(Parser.tokens.actual.tokenType)
            raise Exception("invalid sequence2.2")
            
        return node

    def parseTerm():
        node = Parser.Factor()
        # print(Parser.tokens.actual.tokenType)
        while(Parser.tokens.actual.tokenType == "MULT" or Parser.tokens.actual.tokenType == "DIV"):
            if(Parser.tokens.actual.tokenType == "MULT"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.Factor()])
            if(Parser.tokens.actual.tokenType == "DIV"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.Factor()])
        return node

    def parseExpression():
        node = Parser.parseTerm()
        while(Parser.tokens.actual.tokenType == "PLUS" or Parser.tokens.actual.tokenType == "MINUS"):
            if(Parser.tokens.actual.tokenType == "PLUS"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.parseTerm()])
            elif(Parser.tokens.actual.tokenType == "MINUS"):
                node = BinOp(Parser.tokens.actual.tokenType, [node, Parser.parseTerm()])
        return node

    def parseBlock():
        Parser.tokens.selectNext()
        node = Block()
        if(Parser.tokens.actual.tokenType == "OBLOCK"):
            Parser.tokens.selectNext()
            # print(Parser.tokens.actual.tokenType)
            while(Parser.tokens.actual.tokenType != "CBLOCK"):
                if(Parser.tokens.actual.tokenType == "EOF"):
                    raise Exception("Block not closed")
                node.addChild(Parser.parseStatement())
                Parser.tokens.selectNext()
            Parser.tokens.selectNext()
        else:
            raise Exception("Block not opened")
        return node

    def parseStatement():
        # print(Parser.tokens.actual.tokenType)
        if(Parser.tokens.actual.tokenType == "SC"):
            node = NoOp()
            return node
        elif(Parser.tokens.actual.tokenType == "ID"):
            # print(Parser.tokens.actual.tokenType)
            node = IdOp(Parser.tokens.actual.tokenValue)
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.tokenType == "EQUAL"):
                node = AssignOp([node, Parser.parseExpression()], "=")
                # Parser.tokens.selectNext()
                if(Parser.tokens.actual.tokenType == "SC"):
                    # print(Parser.tokens.actual.tokenType)
                    # node.__repr__()
                    return node
                else:
                    print(Parser.tokens.actual.tokenType)
                    raise Exception("missing semi colon")
            else:
                raise Exception("invalid sequence")
        elif(Parser.tokens.actual.tokenType == "PRINTF"):
            node = PrintOp(Parser.parseExpression())
            if(Parser.tokens.actual.tokenType == "SC"):
                return node
            else:
                raise Exception("missing semi colon")
        else:
            raise Exception("missing semi colon")

    def code_cleanup(code):
        return(re.sub(r'/[*](.*?)[*]/',"", code))
                    
    def run(code):
        Parser.symbolTable = SymbolTable()
        Parser.tokens = Tokenizer(Parser.code_cleanup(code))
        root = Parser.parseBlock()
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