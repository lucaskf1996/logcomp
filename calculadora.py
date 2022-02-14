import sys

def calculadora(eq):
    index = len(eq)
    resultado = 0
    prevNum = 0
    sinal = 0
    for i in range(index):
        if eq[i] == "+":
            if sinal == 0:
                resultado += int(eq[prevNum:i])
            else:
                resultado -= int(eq[prevNum:i])
            sinal = 0
            prevNum = i+1
        if eq[i] == "-":
            if sinal == 0:
                resultado += int(eq[prevNum:i])
            else:
                resultado -= int(eq[prevNum:i])
            sinal = 1
            prevNum = i+1
    if sinal == 0:
        resultado += int(eq[prevNum:])
    else:
        resultado -= int(eq[prevNum:])
    print(resultado)

if __name__ == "__main__":
    calculadora(sys.argv[1])