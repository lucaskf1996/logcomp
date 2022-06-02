class Token:
    def __init__(self, tokenType, tokenValue):
        self.tokenType = tokenType 
        self.tokenValue = tokenValue 

class Tokenizer:

    def __init__(self, origin):
        self.origin = origin 
        self.position = 0
        self.actual = Token(None, None) 
    
    def smallLook(self):
        printteste = 0
        smallLookIndex = self.position
        num=None
        while(len(self.origin)>smallLookIndex):
            if(self.origin[smallLookIndex] == "\n"):
                smallLookIndex+=1
                continue
            elif(self.origin[smallLookIndex].isalpha()):
                alpha = self.origin[smallLookIndex]
                smallLookIndex+=1
                while(smallLookIndex != len(self.origin)):
                    if(self.origin[smallLookIndex].isnumeric() or self.origin[smallLookIndex].isalpha() or self.origin[smallLookIndex] == "_"):
                        alpha = alpha + self.origin[smallLookIndex]
                        smallLookIndex+=1
                    else:
                        if(alpha == "printf"):
                            self.actual = Token("PRINTF", 0)
                            if(printteste): print(self.actual.tokenType)
                            return
                        elif(alpha == "return"):
                            self.actual = Token("RETURN", 0)
                            if(printteste): print(self.actual.tokenType)
                            return
                        elif(alpha == "void"):
                            self.actual = Token("TYPE", 2)
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
            elif(self.origin[smallLookIndex].isnumeric()):
                num = self.origin[smallLookIndex]
                smallLookIndex+=1
                while(smallLookIndex != len(self.origin)):
                    if(self.origin[smallLookIndex].isnumeric()):
                        num = num + self.origin[smallLookIndex]
                        smallLookIndex+=1
                    elif(self.origin[smallLookIndex].isalpha() or self.origin[smallLookIndex] == "_"):
                        raise Exception("invalid number")
                    else:
                        self.actual = Token("NUM", num)
                        if(printteste): print(self.actual.tokenType)
                        return
                self.actual = Token("NUM", num)
                if(printteste): print(self.actual.tokenType)
                return
            elif(self.origin[smallLookIndex] == "\""):
                smallLookIndex+=1
                string = ""
                while(self.origin[smallLookIndex] != "\""):
                    string+=self.origin[smallLookIndex]
                    smallLookIndex+=1
                self.actual = Token("STR", string)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == ","):
                self.actual = Token("COMMA", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "+"):
                self.actual = Token("PLUS", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "-"):
                self.actual = Token("MINUS", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "*"):
                self.actual = Token("MULT", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "/"):
                self.actual = Token("DIV", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "("):
                self.actual = Token("OP", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == ")"):
                self.actual = Token("CP", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "{"):
                self.actual = Token("OBLOCK", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "}"):
                self.actual = Token("CBLOCK", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == ";"):
                self.actual = Token("SC", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "="):
                if(self.origin[smallLookIndex+1] == "="):
                    self.actual = Token("BOOLEQUAL", 0)
                    if(printteste): print(self.actual.tokenType)
                    smallLookIndex+=2
                    return
                else:
                    self.actual = Token("EQUAL", 0)
                    if(printteste): print(self.actual.tokenType)
                    smallLookIndex+=1
                    return
            elif(self.origin[smallLookIndex] == "<"):
                self.actual = Token("LESS", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == ">"):
                self.actual = Token("MORE", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "&"):
                if(self.origin[smallLookIndex+1] == "&"):
                    self.actual = Token("AND", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=2
                return
            elif(self.origin[smallLookIndex] == "|"):
                if(self.origin[smallLookIndex+1] == "|"):
                    self.actual = Token("OR", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=2
                return
            elif(self.origin[smallLookIndex] == "!"):
                self.actual = Token("NOT", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == "."):
                self.actual = Token("CONCAT", 0)
                if(printteste): print(self.actual.tokenType)
                smallLookIndex+=1
                return
            elif(self.origin[smallLookIndex] == " "):
                smallLookIndex+=1
                continue
            elif(self.origin[smallLookIndex] == "\n"):
                smallLookIndex+=1
                continue
            else:
                # print(self.origin[self.position])
                raise Exception("Invalid char")
        self.actual = Token("EOF", 0)
        return

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
                        elif(alpha == "return"):
                            self.actual = Token("RETURN", 0)
                            if(printteste): print(self.actual.tokenType)
                            return
                        elif(alpha == "void"):
                            self.actual = Token("TYPE", 2)
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