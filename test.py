from pprint import pprint


def open_file():
    sourceCode = open("input.txt", "r")
    data = sourceCode.read()
    sourceCode.close()
    return data


sourceCode = open_file().lower()

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

}

sourceCodeChars = list(sourceCode)
tokenList = []
i = 0


def stringProcess(i):
    temp = sourceCodeChars[i:]
    string = ""
    for index, char in enumerate(temp):
        if char == "\"":
            return index + 1, string
        string += char


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
    return type, string


def alphaProcess(i):
    temp = sourceCodeChars[i:]
    type = "WORD"
    string = ""
    for index, char in enumerate(temp):

        if char in " {}" or (char == ":" and not tokenTypes.get(string + ":")):
            break

        if char not in "\n\t":
            string += char

        if tokenTypes.get(string) and temp[index + 1] != ":":
            type = tokenTypes[string]
            break

    if string.__contains__("@"):
        type = "EMAIL"

    return type, string


while i < len(sourceCodeChars):
    char = sourceCodeChars[i]
    if char in " \n\t\r":
        i += 1
    elif char == "*":
        tokenList.append(("STAR", "*"))
        i += 1
    elif char in "+-":
        tokenList.append(("OPERAND", char))
        i += 1
    elif char == ":":
        tokenList.append(("ASSIGN", char))
        i += 1
    elif char == "{":
        tokenList.append(("LEFTBRACE", char))
        i += 1
    elif char == "}":
        tokenList.append(("RIGHTBRACE", char))
        i += 1
    elif char == "\"":
        i, char = stringProcess(i + 1)
        tokenList.append(("STRING", char))
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
