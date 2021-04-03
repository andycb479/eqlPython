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
    if char == "*" and not sourceCodeChars[i + 1].isnumeric():
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
    elif char.isnumeric() or (char == "*" and sourceCodeChars[i + 1].isnumeric()):
        type, char = intProcess(i)
        tokenList.append((type, char))
        i += len(char)
        continue
    elif char.isalpha():
        type, char = alphaProcess(i)
        tokenList.append((type, char))
        i += len(char)


# def parse():
#     input = [token[0] for token in tokenList] + ["$"]
#     stack = ["$", "program"]
#     while True:
#         try:
#             current = parseTable[stack[-1]][input[0]]
#             current.reverse()
#         except:
#             break
#         if current:
#             stack.pop()
#             stack += current
#     print(stack)

def parse():
    flag = 0
    input = [token[0] for token in tokenList] + ["$"]
    stack = ["$", "program"]
    index = 0
    while len(stack) > 0:
        top = stack[len(stack) - 1]
        current_input = input[index]
        if top == current_input:
            stack.pop()
            index = index + 1
        else:
            try:
                current = parseTable[stack[-1]][input[0]]
                current.reverse()
            except:
                flag = 1
                break
            if current != '@':
                current = current[::-1]
                stack.pop()
                stack += current
            else:
                stack.pop()
    if flag == 0:
        print("String accepted")
    else:
        print("String not accepted")


parse()

# def Parser(stack):
#     for token in input:









