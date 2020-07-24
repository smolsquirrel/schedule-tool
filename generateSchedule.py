from itertools import product


def checkValid(lst):
    validList = []
    prodItr = product(*lst)
    for combination in prodItr:
        checkResult = checkAvail(combination)
        if checkResult:
            validList.append(checkResult)
        else:
            continue

    return validList


def checkAvail(courses):
    availability = {"M": {}, "T": {}, "W": {}, "H": {}, "F": {}, "S": {}}
    perm = []
    for course in courses:
        daytime = course.daytimes
        for key in daytime:
            for block in daytime[key]:
                if block in availability[key]:
                    return False
                else:
                    availability[key][block] = True
        perm.append(course)
    return perm
