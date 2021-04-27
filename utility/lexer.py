import datetime
import re
import sys

from utility.grammar.tokenDictionary import tokenTypes
from utility.helpers import open_file


def stringProcess(i, sourceCodeChars):
    temp = sourceCodeChars[i:]
    string = ""
    for index, char in enumerate(temp):
        if char == "\"":
            break
        string += char
    return string


def intProcess(i, sourceCodeChars, lineCount, position):
    temp = sourceCodeChars[i:]
    string = ""
    type = "INT"
    for char in temp:
        if char.isnumeric() or char in "-.dy*":
            string += char
        else:
            break

    if string.__contains__("-") and not string.__contains__("*"):
        try:
            datetime.datetime.strptime(string, '%d-%m-%Y')
            type = "DATE"
        except ValueError:
            print(
                '\033[1;31m' + f"Incorrect date or date format, should be DD-MM-YYYY, line {lineCount} [{position}:{position + len(string)}]")
            sys.exit(1)

    if string.__contains__("y"):
        type = "YEAR"

    if string.__contains__("d"):
        type = "DAY"

    if string.__contains__("*"):
        type = "DATESTRING"

    if string.__contains__("."):
        pattern = re.compile("[0-9]+..[1-9]+")
        if pattern.search(string):
            type = "INTERVAL"
        else:
            print('\033[1;31m' + f"Invalid interval, line {lineCount} [{position}:{position + len(string)}]")
            sys.exit(1)

    return type, string


def alphaProcess(i, sourceCodeChars, lineCount, position):
    temp = sourceCodeChars[i:]
    type = "WORD"
    string = ""
    for index, char in enumerate(temp):

        if char in " {}()+\n" or (char == ":" and not tokenTypes.get(string + ":")):
            break

        if char not in "\n\t":
            string += char

        if (tokenTypes.get(string.lower()) and temp[index + 1] != ":") or \
                tokenTypes.get(string.lower()) and temp[index + 1] == "(":
            type = tokenTypes[string.lower()]
            break

    if string.__contains__("@"):
        pattern = re.compile("\w+@\w+[.]+[a-zA-Z]+")
        if pattern.search(string):
            type = "EMAIL"
        else:
            print('\033[1;31m' + f"Invalid Email format, line {lineCount} [{position}:{position + len(string)}]")
            sys.exit(1)

    return type, string


def lexer(sourcecode):
    tokenList = list()

    sourceCodeChars = open_file(sourcecode)

    i = 0

    lineCount = 1
    position = 1

    while i < len(sourceCodeChars):
        char = sourceCodeChars[i]
        if char == "*" and (not sourceCodeChars[i + 1].isnumeric() and sourceCodeChars[i + 1] not in 'dy'):
            tokenList.append(("STAR", char, lineCount, position, position + 1))
            i += 1
            position += 1
        elif char in " \t\r":
            i += 1
            position += 1
        elif char in "\n":
            position = 1
            lineCount += 1
            i += 1
        elif tokenTypes.get(char):
            tokenList.append((tokenTypes.get(char), char, lineCount, position, position + 1))
            i += 1
            position += 1
        elif char == "\"":
            char = stringProcess(i + 1, sourceCodeChars)
            lenStr = len(char) + 2
            tokenList.append(("STRING", char, lineCount, position, position + lenStr))
            i += lenStr
            position += lenStr
        elif char.isnumeric() or (
                char == "*" and (sourceCodeChars[i + 1].isnumeric() or sourceCodeChars[i + 1] in 'dy')):
            type, char = intProcess(i, sourceCodeChars, lineCount, position)
            lenStr = len(char)
            tokenList.append((type, char, lineCount, position, position + lenStr))
            i += lenStr
            position += lenStr
            continue
        elif char.isalpha():
            type, char = alphaProcess(i, sourceCodeChars, lineCount, position)
            lenStr = len(char)
            tokenList.append((type, char, lineCount, position, position + lenStr))
            i += lenStr
            position += lenStr
        elif char == ".":
            print('\033[1;31m' + f"Invalid input, line {lineCount} [{position}:{position + 1}]")
            sys.exit(1)

    return tokenList
