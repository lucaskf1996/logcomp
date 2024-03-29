class FunctionTable:
    def __init__(self):
        self.table = {}
    
    def getValue(self, identifier):
        try:
            return tuple(self.table[identifier])
        except:
            raise Exception("variable is not declared")
    
    def setValue(self, identifier, value):
        # print(value)
        if(identifier in self.table.keys()):
            self.table[identifier][0] = value
        else:
            raise Exception("variable is not declared")

    def create(self, identifier, value):
        if(identifier in self.table.keys()):
            raise Exception("variable cannot be redeclared")
        if(value == 0):
            self.table[identifier] = [None, "int"]
        elif(value == 1):
            self.table[identifier] = [None, "str"]
        elif(value == 2):
            self.table[identifier] = [None, "void"]