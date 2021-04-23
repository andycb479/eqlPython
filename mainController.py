from pprint import pprint

from utility.helpers import stringTree, printStatements
from utility.lexer import lexer
from utility.parseTreeTraversal import traverse
from utility.parser import parse
from utility.repl import interpretCode
# from eqlPython.utility.helpers import stringTree, printStatements
# from eqlPython.utility.lexer import lexer
# from eqlPython.utility.parseTreeTraversal import traverse
# from eqlPython.utility.parser import parse
# from eqlPython.utility.repl import interpretCode

tokenList = lexer("input.txt")

# print(tokenList)

parseTree = parse(tokenList)

# print(stringTree(parseTree,0))

statements = traverse(parseTree)


interpretCode(statements)
# #
#printStatements(statements)
