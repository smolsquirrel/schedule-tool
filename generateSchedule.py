def checkValid(lst: list) -> list:
    count = 0
    validList = []
    t1, t2, t3, t4, t5, t6, t7 = lst
    for c1 in t1:
        for c2 in t2:
            for c3 in t3:
                for c4 in t4:
                    for c5 in t5:
                        for c6 in t6:
                            for c7 in t7:
                                lst = [c1, c2, c3, c4, c5, c6, c7]
                                checkResult = checkAvail(lst)
                                count += 1
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
