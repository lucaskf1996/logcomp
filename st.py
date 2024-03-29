class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def getValue(self, identifier):
        try:
            return tuple(self.table[identifier])
        except:
            raise Exception("variable is not declared")
    
    def setValue(self, identifier, value):
        if(identifier in self.table.keys()):
            if(self.table[identifier][1] == "int" and value[1] == "int"):
                self.table[identifier][0] = value[0]
            else:
                if(value[1] == "str"):
                    self.table[identifier][0] = value[0]
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
        else:
            raise Exception("invalid variable type")