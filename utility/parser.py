import sys

from utility.grammar.parsingTable import parseTable
from utility.dataTypes import NonTerminalNode, TerminalNode


def parse(tokenList):
    input = [token[0] for token in tokenList] + ["$"]

    stack = ["$", "program"]
    index = 0
    parseTree = NonTerminalNode("program")
    currentNonTerminal = parseTree.nodeList

    while len(stack) > 0:
        top = stack[-1]
        current_input = input[index]
        if top == current_input:
            stack.pop()
            index += 1
        else:
            if (current_input not in parseTable[top]):
                args = [el for el in parseTable[top].keys() if parseTable[top][el][0] != "@"]
                print('\033[1;31m' + f"{top} Expects as arguments{args}")
                sys.exit(1)
            current = parseTable[top].__getitem__(current_input)
            current.reverse()

            if current[0] not in '@':
                stack.pop()
                stack += current
                current.reverse()
            else:
                stack.pop()

        if not top[0].isupper() and top[0] != "$":

            for instance in NonTerminalNode.instances:
                if top == instance.name and len(instance.nodeList) == 0:
                    currentNonTerminal = instance.nodeList

            temp = []
            for key in current:
                if key[0].isupper():
                    for type, value, *other in tokenList[index:]:
                        if type == key:
                            temp.append(TerminalNode(key, value))
                            break
                elif key[0] == "@":
                    temp.append(TerminalNode(key, "@"))
                else:
                    temp.append(NonTerminalNode(key))
            currentNonTerminal += temp

    del NonTerminalNode.instances

    return parseTree
