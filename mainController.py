from pprint import pprint

from utility.helpers import stringTree, printStatements
from utility.lexer import lexer
from utility.parseTreeTraversal import traverse
from utility.parser import parse
from utility.repl import interpretCode

tokenList = lexer("input.txt")

# pprint(tokenList)

parseTree = parse(tokenList)

statements = traverse(parseTree)


interpretCode(statements)
#
# # printStatements(statements)
