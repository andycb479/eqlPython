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