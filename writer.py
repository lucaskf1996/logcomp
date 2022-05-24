import os
class Writer():
    def __init__(self, fileName):
        with open("header.asm", 'r') as file:
            header = file.read()
        self.assembly = header + "\n"
        self.ifNum = 0
        self.whileNum = 0
        self.fileName = fileName

    def write(self, code):
        if("ELSE" in code):
            self.elseNum += 1
        if("WHILE" in code):
            self.whileNum += 1
        self.assembly+="\n"+code

    def end(self):
        with open("end.asm", 'r') as file:
            end = file.read()
        self.assembly += "\n" + end
        with open(f"{self.fileName}.asm", 'w') as file:
            file.write(self.assembly)
        