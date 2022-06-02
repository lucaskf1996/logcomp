from st import SymbolTable
from ft import FunctionTable

class Node():
    def Evaluate(self, symbolTable, funcTable):
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

    def Evaluate(self, symbolTable, funcTable):
        child1 = self.children[0].Evaluate(symbolTable, funcTable)
        child2 = self.children[1].Evaluate(symbolTable, funcTable)
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

    def Evaluate(self, symbolTable, funcTable):
        child = self.children.Evaluate(symbolTable, funcTable)
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

    def Evaluate(self, symbolTable, funcTable):
        if self.value.isnumeric():
            return (int(self.value), "int")
        else:
            raise Exception("Evaluate Error")

class StrVal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print(self.value, " ")

    def Evaluate(self, symbolTable, funcTable):
        return (self.value, "str")

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = None

    def __repr__(self):
        print("No Children")

    def Evaluate(self, symbolTable, funcTable):
        return

class IdOp(Node):
    def __init__(self, value):
        self.value = value
        self.args = []
    
    def __repr__(self):
        print(self.value, " ")

    def addArgs(self, args):
        self.args.append(args)
    
    def Evaluate(self, symbolTable, funcTable):
        if(len(self.args)>0):
            return funcTable.getValue(self.value, self.args)
        else:
            return symbolTable.getValue(self.value) #ja retorna como tupla

class Block(Node):
    def __init__(self):
        self.children = []
        self.value = "block"

    def __repr__(self):
        print("Block children -> ( ")
        for child in self.children:
            child.__repr__()
        print(" ) ")

    def addChild(self, child):
        self.children.append(child)

    def Evaluate(self, symbolTable, funcTable):
        for child in self.children:
            if(child.value == "return"):
                ret = child.Evaluate(symbolTable, funcTable)
                return ret
            child.Evaluate(symbolTable, funcTable)

class PrintOp(Node):
    def __init__(self, child):
        self.value = "print"
        self.child = child
    
    def __repr__(self):
        print("PRINTF", " child -> ( ")
        self.child.__repr__()
        print(" ) ")

    def Evaluate(self, symbolTable, funcTable):
        child = self.child.Evaluate(symbolTable, funcTable)[0]
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

    def Evaluate(self, symbolTable, funcTable):
        symbolTable.setValue(self.children[0].value, self.children[1].Evaluate(symbolTable, funcTable))
        return

class WhileOp(Node):
    def __init__(self, children):
        self.value = "while"
        self.children = children

    def __repr__(self):
        print("WHILE children ->( ")
        self.children[0].__repr__()
        self.children[1].__repr__()
        print(" ) ")
    
    def Evaluate(self, symbolTable, funcTable):
        while(self.children[0].Evaluate(symbolTable, funcTable)[0]):
            # self.children[1].__repr__()
            self.children[1].Evaluate(symbolTable, funcTable)
        return

class IfOp(Node):
    def __init__(self, children):
        self.value = "if"
        self.children = children

    def __repr__(self):
        print("IF children ->( ")
        self.children[0].__repr__()
        self.children[1].__repr__()
        if(self.children[2] != None):
            self.children[2].__repr__()
        print(" ) ")
    
    def Evaluate(self, symbolTable, funcTable):
        if(self.children[0].Evaluate(symbolTable, funcTable)[0]):
            self.children[1].Evaluate(symbolTable, funcTable)
        else:
            self.children[2].Evaluate(symbolTable, funcTable)
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

    def Evaluate(self, symbolTable, funcTable):
        for i in self.children:
            symbolTable.create(i.value, self.value)

class ScanOp(Node):
    def __init__(self):
        self.value = "scan"

    def __repr__(self):
        print("SCAN")
    
    def Evaluate(self, symbolTable, funcTable):
        try:
            inp = int(input())
        except:
            raise Exception("not a int")
        return (inp, "int")

class Program(Node):

    def __init__(self):
        self.children = []

    def addChild(self, node):
        self.children.append(node)
    
    def Evaluate(self, symbolTable, funcTable):
        # print(self.children)
        for child in self.children:
            # print(child)
            child.Evaluate(symbolTable, funcTable)


class FuncDec(Node):

    def __init__(self, value, args, block):
        self.value = value
        self.args = args
        self.block = block
    
    def Evaluate(self, symbolTable, funcTable):
        # print(self.value)
        funcTable.create(self.value[0], self.value[1])
        funcTable.setValue(self.value[0], self)

class FuncCall(Node):

    def __init__(self, value, args):
        self.value = value
        self.args = args
        # print(len(args))
        self.LocalST = SymbolTable()
    
    def Evaluate(self, symbolTable, funcTable):
        func = funcTable.getValue(self.value)
        # for i in self.args:
        #     print(i.value)
        ids = []
        # print(symbolTable.table)
        if len(self.args) == len(func[0].args):
            if(len(self.args) == 0):
                return func[0].block.Evaluate(self.LocalST, funcTable)
            else:
                for arg in func[0].args:
                    # print(arg.children[0].value)
                    arg.Evaluate(self.LocalST, funcTable)
                    # print(arg.children[0].value)
                    ids.append(arg.children[0].value)
                
                # print(self.LocalST.table)
                for arg, id in zip(self.args, ids):
                    # print(symbolTable.table)
                    # print(type(id))
                    # print(arg.Evaluate(symbolTable, funcTable), id.value)
                    self.LocalST.setValue(id, arg.Evaluate(symbolTable, funcTable))
                return func[0].block.Evaluate(self.LocalST, funcTable)
        else:
            raise Exception("num of args missmatch")

class ReturnOp(Node):
    def __init__(self, value, child):
        self.value = value
        self.child = child

    def Evaluate(self, symbolTable, funcTable):
        # print(type(self.child))
        ret = self.child.Evaluate(symbolTable, funcTable)
        # print(ret)
        return ret