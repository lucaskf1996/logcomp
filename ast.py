
class Node():
    def Evaluate(self, symbolTable, writer):
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

    def Evaluate(self, symbolTable, writer):
        child1 = self.children[0].Evaluate(symbolTable, writer)
        writer.write(f"PUSH EBX")
        child2 = self.children[1].Evaluate(symbolTable, writer)
        writer.write(f"POP EAX")
        # print(child1, child2)
        if self.value == "PLUS":
            if(child1[1] == child2[1] == "int"):
                writer.write(f"ADD EAX, EBX")
                return (child1[0] + child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "MINUS":
            if(child1[1] == child2[1] == "int"):
                writer.write(f"SUB EAX, EBX")
                return (child1[0] - child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "MULT":
            if(child1[1] == child2[1] == "int"):
                writer.write(f"IMUL EAX, EBX")
                return (child1[0] * child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "DIV":
            if(child1[1] == child2[1] == "int"):
                writer.write(f"IDIV EBX")
                return (child1[0] // child2[0], "int")
            else:
                raise Exception("cannot make operation with str")
        elif self.value == "BOOLEQUAL":
            # print(type(self.children[0]), type(self.children[1]))
            if(child1[1] == child2[1]):
                writer.write(f"CMP EAX, EBX")
                writer.write(f"CALL binop_je")
                if(child1[0] == child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "LESS":
            if(child1[1] == child2[1]):
                writer.write(f"CMP EAX, EBX")
                writer.write(f"CALL binop_jl")
                if(child1[0] < child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "MORE":
            if(child1[1] == child2[1]):
                writer.write(f"CMP EAX, EBX")
                writer.write(f"CALL binop_jg")
                if(child1[0] > child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "OR":
            if(child1[1] == child2[1]):
                writer.write(f"CALL bool_transform")
                writer.write(f"ADD EBX, EAX")
                writer.write(f"CMP EBX, 0")
                writer.write(f"CALL binop_jg")
                if(child1[0] or child2[0]):
                    return (1, "int")
                else:
                    return (0, "int")
            else:
                raise Exception("cannot compare int with str")
        elif self.value == "AND":
            if(child1[1] == child2[1]):
                writer.write(f"CALL bool_transform")
                writer.write(f"ADD EBX, EAX")
                writer.write(f"CMP EBX, 2")
                writer.write(f"CALL binop_je")
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

    def Evaluate(self, symbolTable, writer):
        child = self.children.Evaluate(symbolTable, writer)
        if child[1] != "int":
            raise Exception("cannot make operation with str")
        if self.value == "PLUS":
            writer.write(f"MOV EBX, {child[0]}")
            return (child[0], "int")
        elif self.value == "MINUS":
            writer.write(f"NEG EBX;")
            return (-child[0], "int")
        elif self.value == "NOT":
            writer.write(f"NOT EBX;")
            return (not child[0], "int")
        else:
            raise Exception("Evaluate Error")

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print(int(self.value), " ")

    def Evaluate(self, symbolTable, writer):
        if self.value.isnumeric():
            writer.write(f"MOV EBX, {int(self.value)}")
            return (int(self.value), "int")
        else:
            raise Exception("Evaluate Error")

class StrVal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        print(self.value, " ")

    def Evaluate(self, symbolTable, writer):
        return (self.value, "str")

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = None

    def __repr__(self):
        print("No Children")

class IdOp(Node):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        print(self.value, " ")
    
    def Evaluate(self, symbolTable, writer):
        id = symbolTable.getValue(self.value)
        writer.write(f"MOV EBX, {id[2]}")
        # writer.write(f"MOV [{id[2]}], EBX")
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

    def Evaluate(self, symbolTable, writer):
        for child in self.children:
            child.Evaluate(symbolTable, writer)

class PrintOp(Node):
    def __init__(self, child):
        self.child = child
    
    def __repr__(self):
        print("PRINTF", " child -> ( ")
        self.child.__repr__()
        print(" ) ")

    def Evaluate(self, symbolTable, writer):
        writer.write(f"\n")
        child = self.child.Evaluate(symbolTable, writer)[0]
        writer.write(f"PUSH EBX")
        writer.write(f"CALL print")
        writer.write(f"POP EBX")
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

    def Evaluate(self, symbolTable, writer):
        writer.write(f"\n")
        child = self.children[1].Evaluate(symbolTable, writer)
        id = symbolTable.getValue(self.children[0].value)[2]
        symbolTable.setValue(self.children[0].value, child)
        # writer.write(f"MOV EBX, {child[0]}")
        writer.write(f"MOV {id}, EBX")
        return

class WhileOp(Node):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        print("WHILE children ->( ")
        self.children[0].__repr__()
        self.children[1].__repr__()
        print(" ) ")
    
    def Evaluate(self, symbolTable, writer):
        writer.write(f"\n")
        writer.write(f"WHILE{writer.whileNum}:")
        self.children[0].Evaluate(symbolTable, writer)[0]
        writer.write(f"CMP EBX, False")
        writer.write(f"JE ENDWHILE{writer.whileNum}")
        self.children[1].Evaluate(symbolTable, writer)
        writer.write(f"JMP WHILE{writer.whileNum}")
        writer.write(f"ENDWHILE{writer.whileNum}")
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
    
    def Evaluate(self, symbolTable, writer):
        self.children[0].Evaluate(symbolTable, writer)[0]
        writer.write(f"\n")
        writer.write(f"CMP EBX, True")
        writer.write(f"JNE IF{writer.ifNum};")
        self.children[2].Evaluate(symbolTable, writer)
        writer.write(f"JMP ENDIF{writer.ifNum}")
        writer.write(f"IF{writer.ifNum}:")
        self.children[1].Evaluate(symbolTable, writer)
        writer.write(f"ENDIF{writer.ifNum}:")
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

    def Evaluate(self, symbolTable, writer):
        for i in self.children:
            symbolTable.create(i.value, self.value)
            writer.write(f"PUSH DWORD 0")

class ScanOp(Node):

    def __repr__(self):
        print("SCAN")
    
    def Evaluate(self, symbolTable, writer):
        try:
            inp = int(input())
        except:
            raise Exception("not a int")
        return (inp, "int")