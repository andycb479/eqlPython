import weakref
from pprint import pprint

from eqlPython.utility.parser import parseTable


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
        return f"{self.name.upper()} " + "\"" + self.value + "\""


def printTree(node, level):
    res = ""

    if not isinstance(node, NonTerminalNode):
        return "\t" * level + str(node) + "\n"

    for child in node.nodeList:
        res = "\t" * level + str(node) + "\n"
        for child in node.nodeList:
            res += printTree(child, level + 1)
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

    traverse(parseTree)


class Filter:
    def __init__(self, name, values):
        self.name = name
        self.values = values


class Expression:
    def __init__(self, assigned, terms):
        self.assigned = assigned
        self.terms = terms


class Print:
    def __init__(self, op):
        self.op = op


Objects = []
prevAssignWord = ""
Content = []
resultWordList = []
fieldsFilter = []
valuesFilter = []
termsExpression = []
assignedExpression = 0
words = []
destinations = []


def find_word_list(node):
    global resultWordList
    for element in node.nodeList:
        if element.name == "WORD":
            resultWordList.append(element.value)
            words.append(element.value)
        elif element.name == "wordlist":
            find_word_list(element)
        else:
            return resultWordList


def find_destination_list(node):
    global destinations
    for element in node.nodeList:
        if element.name == "WORD":
            destinations.append(element.value)
        elif element.name == "destinationvalue":
            find_destination_list(element)
        else:
            return destinations


def find_filter(node):
    global fieldsFilter
    global valuesFilter
    global words
    for element in node.nodeList:
        if element.name == "LEFTBRACE" or element.name == "RIGHTBRACE":
            continue
        elif element.name in "TO FROM CC FORWARDED READ BODY ATTACHMENTS TIME SUBJECT SORTBY FOLDER":
            fieldsFilter.append(element.value)
        elif element.name in "wordlist":
            find_word_list(element)
            valuesFilter.append(words.copy())
            words.clear()
        elif element.name in "destinationvalue":
            find_destination_list(element)
            valuesFilter.append(destinations.copy())
            destinations.clear()
        elif element.name in "WORD BOOLVALUE PARAMETER DATE DATESTRING INTERVAL YEAR DATE EMAIL INT STAR STRING":
            valuesFilter.append(element.value)
        elif element.name in "filter queryvalue attachementsvalue textvalue assignvalue datevalue ":
            find_filter(element)
        else:
            return fieldsFilter


def find_expression_elements(node):
    global termsExpression
    for element in node.nodeList:
        if element.name == "WORD" or element.name == "OPERAND":
            termsExpression.append(element.value)
        elif element.name == "expressionterm" \
                or element.name == "expression2":
            find_expression_elements(element)
        else:
            return termsExpression


def traverse(node):
    global prevAssignWord
    global resultWordList
    if hasattr(node, 'nodeList'):
        elements = []
        for el in node.nodeList:
            elements.append(el)

        if node.name == "print":
            for el in elements:
                if el.name == "wordlist":
                    resultWordList.clear()
                    find_word_list(el)
                    break
            new_print = Print(resultWordList.copy())
            Objects.append(new_print)

        if node.name == "expression":
            termsExpression.clear()
            find_expression_elements(node)
            new_expression = Expression(prevAssignWord, termsExpression)
            Objects.append(new_expression)

        if node.name == "query":
            fieldsFilter.clear()
            valuesFilter.clear()
            find_filter(node)
            filter_values = dict(zip(fieldsFilter, valuesFilter))
            new_filter = Filter(prevAssignWord, filter_values.copy())
            filter_values.clear()
            Objects.append(new_filter)

        elif node.name == "assignment":
            for el in elements:
                if el.name == "WORD":
                    prevAssignWord = el.value

        for el in elements:
            traverse(el)


parse()

print(Objects[0].name)
pprint(Objects[0].values)
print()
print(Objects[1].name)
pprint(Objects[1].values)
print()
print(Objects[2].assigned)
print(Objects[2].terms)
print()
print("Print")
print(Objects[3].op)
