import sys
from parser import Parser

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
    Parser.run(contents)
    # print(Parser.run(sys.argv[1]))