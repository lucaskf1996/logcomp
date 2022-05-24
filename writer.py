import os
class Writer():
    def __init__(self, fileName):
        with open("header.asm", 'r') as file:
            header = file.read()
        self.assembly = header + "\n"
        self.ifNum = 0
        self.whileNum = 0
        self.fileName = fileName.rsplit('.', 1)[0]

    def write(self, code):
        self.assembly+="\n"+code

    def end(self):
        with open("end.asm", 'r') as file:
            end = file.read()
        self.assembly += "\n" + end
        with open(self.fileName+".asm", 'w') as file:
            file.write(self.assembly)
        
    def getLoopNum(self, loop):
        if(loop):
            loopNum = self.whileNum
            self.whileNum += 1
        else:
            loopNum = self.ifNum
            self.ifNum += 1
        
        return loopNum