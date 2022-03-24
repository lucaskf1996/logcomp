import sys
import re

class Node():
    def Evaluate():
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

    def Evaluate(self):
        if self.value == "PLUS":
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == "MINUS":
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == "MULT":
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == "DIV":
            return self.children[0].Evaluate() // self.children[1].Evaluate()
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

    def Evaluate(self):
        if self.value == "PLUS":
            return self.children[0].Evaluate()
        elif self.value == "MINUS":
            return -self.children[0].Evaluate()
        else:
            raise Exception("Evaluate Error")

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print(self.value, " ")

    def Evaluate(self):
        if self.value.isnumeric():
            return int(self.value)
        else:
            raise Exception("Evaluate Error")

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children    

    def __repr__(self):
        print(self.value, " children -> ")
        self.children.__repr__()
        self.children.__repr__()

    def Evaluate(self):
        if self.value.isnumeric():
            return int(self.value)
        else:
            raise Exception("Evaluate Error")

class Token:
    def __init__(self, tokenType, tokenValue):
        self.tokenType = tokenType #str
        self.tokenValue = tokenValue #int

class Tokenizer:

    def __init__(self, origin):
        self.origin = origin #str
        self.position = 0 #int
        self.actual = Token(None, None) #Token

    def selectNext(self):
        num=None
        while(len(self.origin)>self.position):
            if(self.origin[self.position].isnumeric()):
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
                self.actual = Token("OB", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == ")"):
                self.actual = Token("CB", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == " "):
                self.position+=1
                continue
            else:
                raise Exception("Invalid char")
        self.actual = Token("EOF", 0)
        return
        

class Parser:
    tokens = None

    def Factor():
        Parser.tokens.selectNext()
        if(Parser.tokens.actual.tokenType == "NUM"):
            node = IntVal(Parser.tokens.actual.tokenValue)
            Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "MINUS"):
            node = UnOp(Parser.tokens.actual.tokenType, Parser.Factor())
        elif(Parser.tokens.actual.tokenType == "PLUS"):
            node = UnOp(Parser.tokens.actual.tokenType, Parser.Factor())
        elif(Parser.tokens.actual.tokenType == "OB"):
            node = Parser.parseExpression()
            if(Parser.tokens.actual.tokenType == "CB"):
                Parser.tokens.selectNext()
                return node
            else:
                raise Exception("invalid sequence2.1")
        else:
            raise Exception("invalid sequence2.2")
            
        # print(Parser.tokens.actual.tokenType)
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

    

    def code_cleanup(code):
        return(re.sub(r'/[*](.*?)[*]/',"", code))
                    
    def run(code):
        Parser.tokens = Tokenizer(Parser.code_cleanup(code))
        root = Parser.parseExpression()
        # root.__repr__()
        # print(Parser.tokens.actual.tokenType)
        if(Parser.tokens.actual.tokenType == "EOF"):
            return root.Evaluate()
        else:
            raise Exception("invalid sequence")

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
    print(Parser.run(contents))
    # print(Parser.run(sys.argv[1]))