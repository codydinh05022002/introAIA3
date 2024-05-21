import sys
from textparse import TextParser
from TruthTable import *
from BackChain import *
from ForwardChain import *

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    parser = TextParser(filename)
    try:
        kb, query, symbols = parser.read_input()
    except FileNotFoundError:
        sys.exit(1)

    if method == 'TT':
        engine = TruthTableEngine(kb, query, symbols)
    elif method == 'BC':
        engine = BackwardChainingEngine(kb, query, symbols)
    elif method == 'FC':
        engine = ForwardChainingEngine(kb, query, symbols)
    else:
        print("Invalid method! Please use TT, BC, or FC.")
        sys.exit(1)

    engine.execute_algorithm()
