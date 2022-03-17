import sys
import re

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
                        self.actual = Token("NUM", int(num))
                        return
                self.actual = Token("NUM", int(num))
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
        result = 0
        Parser.tokens.selectNext()
        # print(Parser.tokens.actual.tokenValue)
        if(Parser.tokens.actual.tokenType == "NUM"):
            result = Parser.tokens.actual.tokenValue
            Parser.tokens.selectNext()
            # print(Parser.tokens.actual.tokenType)
        elif(Parser.tokens.actual.tokenType == "MINUS"):
            result-=Parser.Factor()
            # Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "PLUS"):
            result+=Parser.Factor()
            # Parser.tokens.selectNext()
        elif(Parser.tokens.actual.tokenType == "OB"):
            # Parser.tokens.selectNext()
            result = Parser.parseExpression()
            # print(result)
            if(Parser.tokens.actual.tokenType == "CB"):
                Parser.tokens.selectNext()
                # print(Parser.tokens.actual.tokenType)s
                # print(result)
                return result
            else:
                raise Exception("invalid sequence2.1")
        else:
            raise Exception("invalid sequence2.2")
        # print(result)
        return result

    def parseTerm():
        result = Parser.Factor()
        # print(result)
        # print(Parser.tokens.actual.tokenType)
        while(Parser.tokens.actual.tokenType == "MULT" or Parser.tokens.actual.tokenType == "DIV"):
            if(Parser.tokens.actual.tokenType == "MULT"):
                result*=Parser.Factor()
            if(Parser.tokens.actual.tokenType == "DIV"):
                result//=Parser.Factor()
            # elif(Parser.tokens.actual.tokenType == "NUM"):
            #     raise Exception("invalid sequence")
        # print(result)
        return result



    def parseExpression():
        result = Parser.parseTerm()
        while(Parser.tokens.actual.tokenType == "PLUS" or Parser.tokens.actual.tokenType == "MINUS"):
            if(Parser.tokens.actual.tokenType == "PLUS"):
                result+=Parser.parseTerm()
            elif(Parser.tokens.actual.tokenType == "MINUS"):
                result-=Parser.parseTerm()
            # elif(Parser.tokens.actual.tokenType == "NUM"):
            #     raise Exception("invalid sequence")
        # print(result)
        return result

    
    def code_cleanup(code):
        return(re.sub(r'/[*](.*?)[*]/',"", code))
                    
    def run(code):
        Parser.tokens = Tokenizer(Parser.code_cleanup(code))
        # Parser.tokens.selectNext()
        result = Parser.parseExpression()
        if(Parser.tokens.actual.tokenType == "EOF"):
            return(result)
        else:
            # print(Parser.tokens.actual.tokenValue)
            raise Exception("invalid sequence")

if __name__ == "__main__":
    print(Parser.run(sys.argv[1]))