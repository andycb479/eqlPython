# grammar = {
#     "program": [["@"], ["statement", "program"]],  # A
#
#     "statement": [["assignment"], ["print"]],  # B
#
#     "assignment": [["WORD", "ASSIGN", "X1"]],  # C
#     "X1": [["query"], ["expression"]],  # ADDED NEW Â
#
#     "query": [["LEFTBRACE", "query", "RIGHTBRACE"],  # D
#               ["filter", "query"],
#               ["filter"],
#               ["@"],
#               ["STAR"]],
#
#     "print": [["PRINT", "LEFTP", "X2", "RIGHTP"]],
#
#     "X2": [["query"], ["WORD"]],  # ADDED NEW
#
#     "expression": [["expression", "OPERAND", "expression"],  # F
#                    ["query"],
#                    ["WORD"]],
#     "filter": [["destination"], ["time"],  # G
#                ["subject"], ["property"],
#                ["content"], ["sorting"],
#                ["folder"]],
#
#     "destination": [["to"], ["from"], ["cc"]],  # H
#     "time": [["TIME", "datevalue"]],  # I
#     "subject": [["SUBJECT", "subjectvalue"]],  # J
#     "sorting": [["SORTBY", "sortingvalue"]],  # K
#     "folder": [["FOLDER", "foldervalue"]],  # L
#     "property": [["forwarded"], ["read"]],  # M
#     "content": [["body"], ["attachments"]],  # N
#     "to": [["TO", "destinationvalue"]],  # O
#     "from": [["FROM", "destinationvalue"]],  # P
#     "cc": [["CC", "destinationvalue"]],  # Q
#     "forwarded": [["FORWARDED", "BOOLVALUE"]],  # R
#     "read": [["READ", "BOOLVALUE"]],  # S
#     "body": [["BODY", "bodyvalue"]],  # T
#     "attachments": [["ATTACHMENTS", "attachementsvalue"]],  # U
#
#
#     "datevalue": [["DATE", "X2"]  # V
#                   ["X2"],
#                   ["STAR", "X3"], ["X3", "STAR"]],
#
#     "X2":[["STAR","DATE"],["STAR"],["@"]],
#     "X3":[["YEAR"],["DAY"]],
#
#
#     "subjectvalue": [["wordlist", "STRING"]],  # W
#     "sortingvalue": [["PARAMETER", "SORTVALUE"]],  # X
#     "foldervalue": [["STRING"]],  # Ș
#     "destinationvalue": [["wordlist"], ["EMAIL"], ["STRING"],  # Y
#                          ["WORD"], ["STAR"]],
#     "bodyvalue": [["wordlist"], ["WORD"], ["STRING"]],  # Z
#     "attachmentsvalue": [["BOOLVALUE"], ["STRING"],  # Ă
#                          ["WORD"], ["INT"], ["INTEVRAL"]],
#     # FEXTENSION TO BE DISSCUSED
#     "wordlist": [["WORD", "wordlist"], ["WORD"], ["@"]]  # Î
# }

parseTable = {
    "program": {
        "PRINT": ["statement", "program"],
        "WORD": ["statement", "program"],
        "$": ["@"]
    },
    "statement": {"PRINT": ["print"], "WORD": ["assignment"]},  # B
    "assignment": {"WORD": ["WORD", "ASSIGN", "assignvalue"]},
    "assignvalue": {"WORD": ["expression"], "LEFTBRACE": ["query"]},
    "query": {"LEFTBRACE": ["LEFTBRACE", "queryvalue", "RIGHTBRACE"]},
    "queryvalue": {
        "ATTACHMENTS": ["filter", "queryvalue"],
        "CC": ["filter", "queryvalue"],
        "SUBJECT": ["filter", "queryvalue"],
        "FROM": ["filter", "queryvalue"],
        "SORTBY": ["filter", "queryvalue"],
        "READ": ["filter", "queryvalue"],
        "TO": ["filter", "queryvalue"],
        "BODY": ["filter", "queryvalue"],
        "FOLDER": ["filter", "queryvalue"],
        "RIGHTBRACE": ["@"],
        "TIME": ["filter", "queryvalue"],
        "FORWARDED": ["filter", "queryvalue"]
    },
    "print": {"PRINT": ["PRINT", "LEFTP", "wordlist", "RIGHTP"]},
    "expression": {"WORD": ["expressionterm", "expression2"]},
    "filter": {
        "ATTACHMENTS": ["ATTACHMENTS", "attachementsvalue"],
        "CC": ["CC", "destinationvalue"],
        "SUBJECT": ["SUBJECT", "textvalue"],
        "FROM": ["FROM", "destinationvalue"],
        "SORTBY": ["SORTBY", "PARAMETER", "SORTVALUE"],
        "READ": ["READ", "BOOLVALUE"],
        "TO": ["TO", "destinationvalue"],
        "BODY": ["BODY", "textvalue"],
        "FOLDER": ["FOLDER", "STRING"],
        "TIME": ["TIME", "datevalue"],
        "FORWARDED": ["FORWARDED", "BOOLVALUE"]
    },
    "textvalue": {
        "ATTACHMENTS": ["wordlist"],
        "CC": ["wordlist"],
        "SUBJECT": ["wordlist"],
        "FROM": ["wordlist"],
        "STRING": ["STRING"],
        "SORTBY": ["wordlist"],
        "READ": ["wordlist"],
        "TO": ["wordlist"],
        "WORD": ["wordlist"],
        "BODY": ["wordlist"],
        "FOLDER": ["wordlist"],
        "RIGHTBRACE": ["wordlist"],
        "TIME": ["wordlist"],
        "FORWARDED": ["wordlist"]
    },
    "destinationvalue": {
        "STAR": ["STAR"],
        "ATTACHMENTS": ["@"],
        "CC": ["@"],
        "SUBJECT": ["@"],
        "FROM": ["@"],
        "EMAIL": ["EMAIL", "destinationvalue"],
        "SORTBY": ["@"],
        "READ": ["@"],
        "TO": ["@"],
        "WORD": ["WORD", "destinationvalue"],
        "BODY": ["@"],
        "FOLDER": ["@"],
        "RIGHTBRACE": ["@"],
        "TIME": ["@"],
        "FORWARDED": ["@"]
    },
    "attachementsvalue": {
        "ATTACHMENTS": ["wordlist"],
        "BOOLVALUE" : ["BOOLVALUE"],
        "CC": ["wordlist"],
        "SUBJECT": ["wordlist"],
        "FROM": ["wordlist"],
        "INTERVAL": ["INTERVAL"],
        "SORTBY": ["wordlist"],
        "READ": ["wordlist"],
        "TO": ["wordlist"],
        "INT": ["INT"],
        "WORD": ["wordlist"],
        "BODY": ["wordlist"],
        "FOLDER": ["wordlist"],
        "RIGHTBRACE": ["wordlist"],
        "TIME": ["wordlist"],
        "FORWARDED": ["wordlist"]
    },
    "wordlist": {
        "RIGHTP": ["@"],
        "ATTACHMENTS": ["@"],
        "CC": ["@"],
        "SUBJECT": ["@"],
        "FROM": ["@"],
        "SORTBY": ["@"],
        "READ": ["@"],
        "TO": ["@"],
        "WORD": ["WORD", "wordlist"],
        "BODY": ["@"],
        "FOLDER": ["@"],
        "RIGHTBRACE": ["@"],
        "TIME": ["@"],
        "FORWARDED": ["@"]
    },
    "expression2": {
        "PRINT": ["@"],
        "OPERAND": ["OPERAND", "expressionterm", "expression2"],
        "WORD": ["@"],
        "$": ["@"]
    },
    "expressionterm": {"WORD": ["WORD"]},
    "datevalue": {
        "DATE": ["DATE"],
        "YEAR": ["YEAR"],
        "DAY": ["DAY"],
        "DATESTRING": ["DATESTRING"]
    }
}
