from pprint import pprint

from utility.helpers import stringTree, printStatements
from utility.lexer import lexer
from utility.parseTreeTraversal import traverse
from utility.parser import parse


tokenList = lexer("input.txt")

print(tokenList)

parseTree = parse(tokenList)

#print(stringTree(parseTree,1))

statements = traverse(parseTree)

printStatements(statements)
