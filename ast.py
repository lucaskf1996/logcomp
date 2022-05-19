
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
        child1 = self.children[0].Evaluate(symbolTable)
        child2 = self.children[1].Evaluate(symbolTable)
        # print(child1, child2)
        if self.value == "PLUS":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] + child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "MINUS":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] - child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "MULT":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] * child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "DIV":
            if(child1[1] == child2[1] == "int"):
                return (child1[0] // child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "BOOLEQUAL":
            # print(type(self.children[0]), type(self.children[1]))
            if(child1[1] == child2[1]):
                if(child1[0] == child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "LESS":
            if(child1[1] == child2[1]):
                if(child1[0] < child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "MORE":
            if(child1[1] == child2[1]):
                if(child1[0] > child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "OR":
            if(child1[1] == child2[1]):
                if(child1[0] or child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "AND":
            if(child1[1] == child2[1]):
                if(child1[0] and child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "CONCAT":
            return (str(child1[0]) + str(child2[0]), "str")
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
        child = self.children.Evaluate(symbolTable)
        if child[1] != "int":
            raise Exception("cannot make operation with str")
        if self.value == "PLUS":
            return (child[0], "int")
        elif self.value == "MINUS":
            return (-child[0], "int")
        elif self.value == "NOT":
            return (not child[0], "int")
        else:
            raise Exception("Evaluate Error")

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print(int(self.value), " ")

    def Evaluate(self, symbolTable):
        if self.value.isnumeric():
            return (int(self.value), "int")
        else:
            raise Exception("Evaluate Error")

class StrVal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print(self.value, " ")

    def Evaluate(self, symbolTable):
        return (self.value, "str")

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
        return symbolTable.getValue(self.value) #ja retorna como tupla

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
        child = self.child.Evaluate(symbolTable)[0]
        print(child)

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

class WhileOp(Node):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        print("WHILE children ->( ")
        self.children[0].__repr__()
        self.children[1].__repr__()
        print(" ) ")
    
    def Evaluate(self, symbolTable):
        while(self.children[0].Evaluate(symbolTable)[0]):
            # self.children[1].__repr__()
            self.children[1].Evaluate(symbolTable)
        return

class IfOp(Node):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        print("IF children ->( ")
        self.children[0].__repr__()
        self.children[1].__repr__()
        if(self.children[2] != None):
            self.children[2].__repr__()
        print(" ) ")
    
    def Evaluate(self, symbolTable):
        if(self.children[0].Evaluate(symbolTable)[0]):
            self.children[1].Evaluate(symbolTable)
        else:
            self.children[2].Evaluate(symbolTable)
        return

class VarDec(Node):

    def __init__(self, value):
        self.children = []
        self.value = value

    def __repr__(self):
        print("VarDec children -> ( ")
        for child in self.children:
            child.__repr__()
        print(" ) ")

    def addChild(self, child):
        self.children.append(child)

    def Evaluate(self, symbolTable):
        for i in self.children:
            symbolTable.create(i.value, self.value)

class ScanOp(Node):

    def __repr__(self):
        print("SCAN")
    
    def Evaluate(self, symbolTable):
        try:
            inp = int(input())
        except:
            raise Exception("not a int")
        return (inp, "int")