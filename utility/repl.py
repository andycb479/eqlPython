import datetime
import json
import time
from pathlib import Path
from utility.dataTypes import Filter, Expression, Print
from pprint import pprint

emailDataBase = Path("utility/emailsdb.json").read_text()
filterDataBase = Path("utility/filtersdb.json").read_text()
emails = json.loads(emailDataBase)
filters = json.loads(filterDataBase)


def processStrFields(emailField, field, filter):
    ismatch = False

    fieldvalue = filter[field]

    if fieldvalue[0] == "*":
        return True

    if isinstance(fieldvalue, list):
        flag = False
        for word in fieldvalue:
            flag |= word in emailField or word == emailField
        ismatch |= flag
    else:
        ismatch = fieldvalue in emailField or fieldvalue == emailField

    return ismatch


def processAttachments(emailField, filterValue):
    attachmentsCount = len(emailField)

    ismatch = False

    if isinstance(filterValue, list):
        flag = False

        for word in filterValue:
            for attachment in emailField:
                flag |= word in attachment
        ismatch |= flag
        return ismatch

    if filterValue in "yes no":
        if filterValue == "yes" and attachmentsCount != 0:
            return True
        elif filterValue == "no" and attachmentsCount == 0:
            return True
    elif filterValue.__contains__(".."):
        filterValue = filterValue.split("..")
        if int(filterValue[0]) <= attachmentsCount <= int(filterValue[1]):
            return True
    elif filterValue.isnumeric():
        if int(filterValue) == attachmentsCount:
            return True
    elif filterValue.isalpha():
        pass

    return False


def processSingleStr(emailField, filterValue):
    if emailField == "true" and filterValue.lower() == "yes":
        return True
    elif emailField == "false" and filterValue.lower() == "no":
        return True
    elif filterValue.lower() not in "yes no":
        if emailField == filterValue:
            return True
    return False


def processTime(emailField, filterValue):

    emailDate = datetime.datetime.strptime(emailField, '%Y-%m-%dT%H:%M:%S.%fZ')

    if filterValue.__contains__("*"):

        dates = filterValue.split("*")
        if dates.__contains__(""):

            starIndex = dates.index("")

            if starIndex == 0:
                lower = datetime.datetime.min
                upper = datetime.datetime.strptime(dates[1], '%d-%m-%Y')
            else:
                lower = datetime.datetime.strptime(dates[0], '%d-%m-%Y')
                upper = datetime.datetime.max

        else:
            lower = datetime.datetime.strptime(dates[0], '%d-%m-%Y')
            upper = datetime.datetime.strptime(dates[1], '%d-%m-%Y')

        if lower <= emailDate <= upper:
            return True

    elif datetime.datetime.strptime(filterValue, '%d-%m-%Y').date() == emailDate.date():
        return True


def filterEmails(filter):
    res = list()

    print(filter)

    for email in emails:
        ismatch = False
        for field in filter:
            temp = field.replace(":", "")

            if field in "to: from: cc: subject:":
                if email["header"][temp] == "":
                    ismatch = False
                    break
                ismatch = processStrFields(email["header"][temp], field, filter)

            elif field in "body:":
                ismatch = processStrFields(email["body"]["content"], field, filter)
            elif field in "attachments:":
                ismatch = processAttachments(email["body"]["attachments"], filter[field])
            elif field in "read: forwarded: folder:":
                ismatch = processSingleStr(email["metadata"][temp], filter[field])
            elif field in "time:":
                ismatch = processTime(email["metadata"]["date"], filter[field])

            if not ismatch:
                break

        if ismatch:
            res.append(email)

    return res


def applyFilter(filter):
    res = list()

    if ("to:" in filter) and ("from:" in filter):
        temp = filter.copy()
        temp.pop("to:")
        res.extend(filterEmails(temp))
        filter.pop("from:")
        res.extend(filterEmails(filter))
    else:
        res.extend(filterEmails(filter))

    pprint(res, sort_dicts=False)


def interpretCode(statements):
    for statement in statements:
        if (isinstance(statement, Filter)):
            filters[statement.name] = statement.values # example of adding Filter object to dictionary filters
        elif (isinstance(statement, Expression)):

            #expression processing -> procesExpr()

            #input -> expression (statement)

            #output - > Filter object
            # + add new filter to filters dictionary filters[newfiltername] = output.values


            pass
        elif (isinstance(statement, Print)):
            for filter in statement.words:
                applyFilter(filters[filter])

# Path("utility/filtersdb.json").write_text(json.dumps(filters))
