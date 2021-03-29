from pprint import pprint


def open_file():
    sourceCode = open("input.txt", "r")
    data = sourceCode.read()
    sourceCode.close()
    return data


sourceCode = open_file()

tokenTypes = {
    "time": "PARAMETER",
    "name": "PARAMTER",
    "asc": "SORTVALUE",
    "desc": "SORTVALUE",
    "yes": "BOOLVALUE",
    "no": "BOOLVALUE",
    "to:": "TO",
    "from:": "FROM",
    "cc:": "CC",
    "forwarded:": "FORWARDED",
    "read:": "READ",
    "body:": "BODY",
    "attachements:": "ATTACHEMENTS",
    "time:": "TIME",
    "subject:": "SUBJECT",
    "sortby:": "SORTBY",
    "folder:": "FOLDER",
    "print": "PRINT",
    "+": "OPERAND",
    "-": "OPERAND",
    ":": "ASSIGN",
    "*": "STAR",
    "{": "LEFTBRACE",
    "}": "RIGHTBRACE",
    "(": "LEFTP",
    ")": "RIGHTP"
}

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
        if char.isnumeric() or char in "-.dy":
            string += char
        else:
            break

    if string.__contains__("-"):
        type = "DATE"

    if string.__contains__(".."):
        type = "INTERVAL"

    if string.__contains__("y"):
        type = "YEAR"

    if string.__contains__("d"):
        type = "DAY"

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
    if char in " \n\t\r":
        i += 1
    elif tokenTypes.get(char):
        tokenList.append((tokenTypes.get(char), char))
        i += 1
    elif char == "\"":
        char = stringProcess(i + 1)
        tokenList.append(("STRING", char))
        i += len(char) + 2
    elif char.isnumeric():
        type, char = intProcess(i)
        tokenList.append((type, char))
        i += len(char)
        continue
    elif char.isalpha():
        type, char = alphaProcess(i)
        tokenList.append((type, char))
        i += len(char)


print(sourceCode)
print()
pprint(tokenList)