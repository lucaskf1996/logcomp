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
            elif(self.origin[self.position] == "+" and self.actual.tokenType != "PLUS"):
                self.actual = Token("PLUS", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "-" and self.actual.tokenType != "MINUS"):
                self.actual = Token("MINUS", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "*" and self.actual.tokenType != "MULT"):
                self.actual = Token("MULT", 0)
                self.position+=1
                return
            elif(self.origin[self.position] == "/" and self.actual.tokenType != "DIV"):
                self.actual = Token("DIV", 0)
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

    def parseTerm():
        result = 0
        Parser.tokens.selectNext()
        # print(Parser.tokens.actual.tokenType+'1')
        if(Parser.tokens.actual.tokenType == "NUM"):
            result = Parser.tokens.actual.tokenValue
            Parser.tokens.selectNext()
            # print(Parser.tokens.actual.tokenType+'2')
            if(Parser.tokens.actual.tokenType == "MULT" or Parser.tokens.actual.tokenType == "DIV"):
                while(Parser.tokens.actual.tokenType == "MULT" or Parser.tokens.actual.tokenType == "DIV"):
                    if(Parser.tokens.actual.tokenType == "MULT"):
                        Parser.tokens.selectNext()
                        # print(Parser.tokens.actual.tokenType+'3')
                        if(Parser.tokens.actual.tokenType == "NUM"):
                            result*=Parser.tokens.actual.tokenValue
                        else:
                            raise Exception("invalid sequence")
                    if(Parser.tokens.actual.tokenType == "DIV"):
                        Parser.tokens.selectNext()
                        # print(Parser.tokens.actual.tokenType+'4')
                        if(Parser.tokens.actual.tokenType == "NUM"):
                            result/=Parser.tokens.actual.tokenValue
                        else:
                            raise Exception("invalid sequence")
                    Parser.tokens.selectNext()
                    # print(Parser.tokens.actual.tokenType+'5')
                return result
            else:
                return result
        else:
            raise Exception("invalid sequence")



    def parseExpression():
        result = 0
        result += Parser.parseTerm()
        while(True):
            if(Parser.tokens.actual.tokenType == "PLUS" or Parser.tokens.actual.tokenType == "MINUS"):
                if(Parser.tokens.actual.tokenType == "PLUS"):
                    result+=Parser.parseTerm()
                elif(Parser.tokens.actual.tokenType == "MINUS"):
                    result-=Parser.parseTerm()
            elif(Parser.tokens.actual.tokenType == "NUM"):
                raise Exception("invalid sequence")
            else:
                return int(result)

    
    def code_cleanup(code):
        return(re.sub(r'/[*](.*?)[*]/',"", code))
                    
    def run(code):
        Parser.tokens = Tokenizer(Parser.code_cleanup(code))
        return(Parser.parseExpression())

if __name__ == "__main__":
    print(Parser.run(sys.argv[1]))