from pprint import pprint
sourceCode = "\"test\" *  + -:25*255 star12 test@gmail.com 21-12-2019"

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
        if char=="-":
            type="DATE"
        if char.isnumeric() or char=="-":
           string += char
        else:
            break
    return type,string


def alphaProcess(i):
    temp = sourceCodeChars[i:]
    type = "WORD"
    string=""
    for char in temp:
        if char == "@":
            type = "EMAIL"
        if char == " ":
            break
        string += char
    return type,string


while i < len(sourceCodeChars):
    char = sourceCodeChars[i]
    if char in " \n\t\r":
        pass
    elif char == "*":
        tokenList.append(("STAR", "*"))
    elif char in "+-":
        tokenList.append(("OPERAND", char))
    elif char == ":":
        tokenList.append(("ASSIGN", char))
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
    i += 1

pprint(tokenList)
