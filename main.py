import sys

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
        while(len(self.origin)!=self.position):
            if(self.origin[self.position].isnumeric()):
                num = self.origin[self.position]
                # print(num)
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
            elif(self.position == self.origin):
                self.actual = Token("EOF", 0)
                return
            elif(self.origin[self.position] == " "):
                self.position+=1
                continue
            else:
                raise Exception("Invalid char")

class Parser:
    tokens = None

    def parseExpression():
        Parser.tokens.selectNext()
        if(Parser.tokens.actual.tokenType == "NUM"):
            result = Parser.tokens.actual.tokenValue
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.tokenType == "PLUS" or Parser.tokens.actual.tokenType == "MINUS"):
                while(True):
                    if(Parser.tokens.actual.tokenType == "PLUS"):
                        Parser.tokens.selectNext()
                        if(Parser.tokens.actual.tokenType == "NUM"):
                            result+=Parser.tokens.actual.tokenValue
                            Parser.tokens.selectNext()
                        else:
                            raise Exception("invalid sequence")
                    if(Parser.tokens.actual.tokenType == "MINUS"):
                        Parser.tokens.selectNext()
                        if(Parser.tokens.actual.tokenType == "NUM"):
                            result-=Parser.tokens.actual.tokenValue
                            Parser.tokens.selectNext()
                        else:
                            raise Exception("invalid sequence")
                    return result
            else:
                raise Exception("invalid sequence")
        else:
            raise Exception("invalid sequence")
                    
    def run(code):
        Parser.tokens = Tokenizer(code)
        return(Parser.parseExpression())

if __name__ == "__main__":
    print(Parser.run(sys.argv[1]))    