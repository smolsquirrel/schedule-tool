import sys
sys.path.append("./models")
from course import Course
from daytime import Daytime
import re

def readFile(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines


def time_conv(time):
    x = time.split(":")
    hour, minute = [int(elem) for elem in x]
    new_minute = (hour * 60) + minute
    return new_minute


def day_time(day, time):
    time_range = list(map(time_conv, time))
    daytime_obj = Daytime(day, time_range[0], time_range[1])
    return daytime_obj


def find_teacher(data):
    if re.search(r"\w+,\s\w+", data[2]):
        teacher = data[2]
        return teacher


range_maker = lambda start, end: range(start, end)


def make_course_list(filename):
    new_line = lambda x: x != ""
    lines = readFile(filename)
    course_list = []
    course_dict = {}
    empty_range = {
        0: range(0, 0),
        1: range(0, 0),
        2: range(0, 0),
        3: range(0, 0),
        4: range(0, 0),
        5: range(0, 0),
    }
    empty_list = {
        "section": "",
        "number": "",
        "name": "",
        "teacher": "",
        "daytimes": empty_range,
    }
    weekdays = {"M": 0, "T": 1, "W": 2, "H": 3, "F": 4, "S": 5}
    temp = empty_list.copy()
    for line in lines:
        data = re.split(
            r',(?!\s|")', line.rstrip()
        )  # splits on comma, except for teacher name
        if data[0] != "":  # check if new course
            x = Course(
                temp["section"],
                temp["number"],
                temp["name"],
                temp["teacher"],
                temp["daytimes"],
            )
            key = "%s / %s" % (temp["number"], temp["section"])
            course_dict[key] = x
            course_list.append(x)
            temp = empty_list.copy()  # resets dict
            temp["daytimes"] = empty_range.copy()
            temp["section"] = data[0]
            temp["number"] = data[1]
            temp["name"] = data[2]
            days = data[3]
            start, end = data[4].split("-")
            for day in days:
                temp["daytimes"][weekdays[day]] = range_maker(
                    time_conv(start), time_conv(end)
                )
        else:
            teacher = find_teacher(data)
            if teacher != None:
                temp["teacher"] = teacher
            if data[3] != "":
                days = data[3]
                start, end = data[4].split("-")
                for day in days:
                    temp["daytimes"][weekdays[day]] = range_maker(
                        time_conv(start), time_conv(end)
                    )

    x = Course(
        temp["section"], temp["number"], temp["name"], temp["teacher"], temp["daytimes"]
    )
    key = "%s / %s" % (temp["number"], temp["section"])
    course_dict[key] = x
    course_list.append(x)
    course_list.pop(0)

    return [course_list, course_dict]


test_list = [
    ["109-102-MQ / 4"],
    ["201-NYA-05 / 12"],
    ["202-NYA-05 / 14"],
    ["203-NYA-05 / 21"],
    ["345-102-MQ / 5"],
    ["603-101-MQ / 1"],
    ["GER-LAL / 1"],
]


def get_times(tab, course_dict):
    tab_list = []
    weekdays = {"M": 0, "T": 1, "W": 2, "H": 3, "F": 4, "S": 5}
    for elem in tab:
        sch = {
            0: range(0, 0),
            1: range(0, 0),
            2: range(0, 0),
            3: range(0, 0),
            4: range(0, 0),
            5: range(0, 0),
        }
        obj = course_dict[elem].daytimes
        for i in obj:
            day, start, end = [i.day, i.start, i.end]
            weekday = weekdays[day]
            sch[weekday] = range(start, end)
        tab_list.append((course_dict[elem], sch))
    return tab_list
