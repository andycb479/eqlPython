import weakref
from utility.parser import parseTable

def open_file():
    sourceCode = open("input.txt", "r")
    data = sourceCode.read()
    sourceCode.close()
    return data

sourceCode = open_file()

tokenTypes = {

    "time": "PARAMETER", "name": "PARAMETER",  # p
    "asc": "SORTVALUE", "desc": "SORTVALUE",  # s
    "yes": "BOOLVALUE", "no": "BOOLVALUE",  # b
    "to:": "TO",  # t
    "from:": "FROM",  # f
    "cc:": "CC",  # c
    "forwarded:": "FORWARDED",  # ș
    "read:": "READ",  # r
    "body:": "BODY",  # y
    "attachments:": "ATTACHMENTS",  # a
    "time:": "TIME",  # ă
    "subject:": "SUBJECT",  # e
    "sortby:": "SORTBY",  # o
    "folder:": "FOLDER",  # z
    "print": "PRINT",  # i
    "+": "OPERAND", "-": "OPERAND",  # n
    ":": "ASSIGN",  # :
    "{": "LEFTBRACE",  # {
    "}": "RIGHTBRACE",  # }
    "(": "LEFTP",  # (
    ")": "RIGHTP"  # )

}

# DATE - d
# INTERVAL - j
# YEAR - m
# DAY - q
# EMAIL - l
# INT - u
# STRING - k
# WORD - w
# DATESTRING - â

sourceCodeChars = list(sourceCode)
tokenList = []
i = 0


def stringProcess(i):
    temp = sourceCodeChars[i:]
    string = ""
    for index, char in enumerate(temp):
        if char == "\"":
            break
        string += char
    return string


def intProcess(i):
    temp = sourceCodeChars[i:]
    string = ""
    type = "INT"
    for char in temp:
        if char.isnumeric() or char in "-.dy*":
            string += char
        else:
            break

    if string.__contains__("-"):
        type = "DATE"

    if string.__contains__("y"):
        type = "YEAR"
    if string.__contains__("d"):
        type = "DAY"

    if string.__contains__("*"):
        type = "DATESTRING"

    if string.__contains__(".."):
        type = "INTERVAL"

    return type, string


def alphaProcess(i):
    temp = sourceCodeChars[i:]
    type = "WORD"
    string = ""
    for index, char in enumerate(temp):

        if char in " {}()\n" or (char == ":" and not tokenTypes.get(string + ":")):
            break

        if char not in "\n\t":
            string += char

        if (tokenTypes.get(string.lower()) and temp[index + 1] != ":") or \
                tokenTypes.get(string.lower()) and temp[index + 1] == "(":
            type = tokenTypes[string.lower()]
            break

    if string.__contains__("@"):
        type = "EMAIL"

    return type, string


while i < len(sourceCodeChars):
    char = sourceCodeChars[i]
    if char == "*" and (not sourceCodeChars[i + 1].isnumeric() and sourceCodeChars[i + 1] not in 'dy'):
        tokenList.append(("STAR", char))
        i += 1
    elif char in " \n\t\r":
        i += 1
    elif tokenTypes.get(char):
        tokenList.append((tokenTypes.get(char), char))
        i += 1
    elif char == "\"":
        char = stringProcess(i + 1)
        tokenList.append(("STRING", char))
        i += len(char) + 2
    elif char.isnumeric() or (char == "*" and sourceCodeChars[i + 1].isnumeric() or sourceCodeChars[i + 1] in 'dy'):
        type, char = intProcess(i)
        tokenList.append((type, char))
        i += len(char)
        continue
    elif char.isalpha():
        type, char = alphaProcess(i)
        tokenList.append((type, char))
        i += len(char)


class NonTerminalNode:
    instances = []

    def __init__(self, name):
        self.name = name
        self.nodeList = []
        self.__class__.instances.append(weakref.proxy(self))

    def __str__(self):
        return f"<{self.name}>"


class TerminalNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name.upper()} " + "\""+self.value+"\""

def printTree(node,level):
    res=""

    if not isinstance(node,NonTerminalNode):
        return "\t" * level + str(node) + "\n"

    for child in node.nodeList:
        res = "\t" * level + str(node) + "\n"
        for child in node.nodeList:
            res += printTree(child,level+1)
        return res




def parse():
    flag = 0
    input = [token[0] for token in tokenList] + ["$"]
    print(input)
    stack = ["$", "program"]
    index = 0
    parseTree = NonTerminalNode("program")
    currentNonTerminal = parseTree.nodeList

    prev = 0
    while len(stack) > 0:
        top = stack[-1]
        current_input = input[index]
        if top == current_input:
            stack.pop()
            index += 1
        else:
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
                    for type, value in tokenList[index:]:
                        if type == key:
                            temp.append(TerminalNode(key, value))
                            break
                elif key[0] == "@":
                    temp.append(TerminalNode(key, "@"))
                else:
                    temp.append(NonTerminalNode(key))
            currentNonTerminal += temp

    del NonTerminalNode.instances

    print(printTree(parseTree, 1))
    if flag == 0:
        print("String accepted")
    else:
        print("String not accepted")



parse()
