grammar = {
    "program": [["@"], ["statement", "program"]],  # A

    "statement": [["assignment"], ["print"]],  # B

    "assignment": [["WORD", "ASSIGN", "X1"]],  # C
    "X1": [["query"], ["expression"]],  # ADDED NEW Â

    "query": [["LEFTBRACE", "query", "RIGHTBRACE"],  # D
              ["filter", "query"],
              ["filter"],
              ["@"],
              ["STAR"]],

    "print": [["PRINT", "LEFTP", "X2", "RIGHTP"]],

    "X2": [["query"], ["WORD"]],  # ADDED NEW

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


    "datevalue": [["DATE", "X2"]  # V
                  ["X2"],
                  ["STAR", "X3"], ["X3", "STAR"]],

    "X2":[["STAR","DATE"],["STAR"],["@"]],
    "X3":[["YEAR"],["DAY"]],


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
