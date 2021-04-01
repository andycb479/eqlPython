grammar = {
    "program": [["@"], ["statement", "program"]],  # A
    "statement": [["assignment"], ["print"]],  # B
    "assignment": [["WORD", "ASSIGN", "query"],  # C
                   ["WORD", "ASSIGN", "expression"]],
    "query": [["LEFTBRACE", "STAR", "RIGHTBRACE"],  # D
              ["LEFTBRACE", "filter", "query", "RIGHTBRACE"],
              ["filter", "query"],
              ["filter"],
              ["@"]],
    "print": [["PRINT", "LEFTP", "query", "RIGHTP"],  # E
              ["PRINT", "LEFTP", "WORD", "RIGHTP"]],
    "expression": [["expression", "OPERAND", "expression"],  # F
                   ["query"],
                   ["WORD"]],
    "filter": [["destination"], ["time"],  # G
               ["subject"], ["property"],
               ["content"], ["sorting"],
               ["folder"]],
    "destination": [["to"], ["from"], ["cc"]],  # H
    "time": [["TIME", "datevalue"]],  # I
    "subject": [["SUBJECT", "subjectvalue"]],  # J
    "sorting": [["SORTBY", "sortingvalue"]],  # K
    "folder": [["FOLDER", "foldervalue"]],  # L
    "property": [["forwarded"], ["read"]],  # M
    "content": [["body"], ["attachments"]],  # N
    "to": [["TO", "destinationvalue"]],  # O
    "from": [["FROM", "destinationvalue"]],  # P
    "cc": [["CC", "destinationvalue"]],  # Q
    "forwarded": [["FORWARDED", "BOOLVALUE"]],  # R
    "read": [["READ", "BOOLVALUE"]],  # S
    "body": [["BODY", "bodyvalue"]],  # T
    "attachments": [["ATTACHMENTS", "attachementsvalue"]],  # U
    "datevalue": [["DATE"], ["DATE", "STAR", "DATE"],  # V
                  ["DATE", "STAR"], ["STAR", "DATE"],
                  ["STAR", "DAY"], ["DAY", "STAR"],
                  ["STAR", "YEAR"], ["YEAR", "STAR"]],
    "subjectvalue": [["wordlist", "STRING"]],  # W
    "sortingvalue": [["PARAMETER", "SORTVALUE"]],  # X
    "foldervalue": [["STRING"]],  # Ș
    "destinationvalue": [["wordlist"], ["EMAIL"], ["STRING"],  # Y
                         ["WORD"], ["STAR"]],
    "bodyvalue": [["wordlist"], ["WORD"], ["STRING"]],  # Z
    "attachmentsvalue": [["BOOLVALUE"], ["STRING"],  # Ă
                         ["WORD"], ["INT"], ["INTEVRAL"]],
    # FEXTENSION TO BE DISSCUSED
    "wordlist": [["WORD", "wordlist"], ["WORD"], ["@"]]  # Î
}

print(grammar[str][0][0], grammar["read"][0][0])
