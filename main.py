import sys
sys.path.append("./models")
from course import Course, Week
import re
import pickle


def readFile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
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


def make_course_list(filename):
    lines = readFile(filename)
    course_list = []
    course_dict = {}
    weekdays = {"M": 0, "T": 1, "W": 2, "H": 3, "F": 4, "S": 5}
    temp = {"section": "", "number": "", "name": "", "teacher": "", "daytimes": ""}
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
            temp["daytimes"] = {}
            temp["section"] = data[0]
            temp["number"] = data[1]
            temp["name"] = data[2]
            days = data[3]
            start, end = data[4].split("-")
            for day in days:
                temp["daytimes"][day] = list(
                    range(time_conv(start), time_conv(end), 30)
                )
        else:
            teacher = find_teacher(data)
            if teacher != None:
                temp["teacher"] = teacher
            if data[3] != "":
                days = data[3]
                start, end = data[4].split("-")
                for day in days:
                    temp["daytimes"][day] = list(
                        range(time_conv(start), time_conv(end), 30)
                    )

    x = Course(
        temp["section"], temp["number"], temp["name"], temp["teacher"], temp["daytimes"]
    )
    key = "%s / %s" % (temp["number"], temp["section"])
    course_dict[key] = x
    course_list.append(x)
    course_list.pop(0)  # removes blank first course

    return [course_list, course_dict]


test_list = [
    ["109-102-MQ / 4"],
    ["201-NYA-05 / 12"],
    ["202-NYA-05 / 14"],
    ["203-NYA-05 / 21"],
    ["345-102-MQ / 5"],
    ["603-101-MQ / 1"],
    ["GER-LAL / 1", "ITA-LAA / 3"],
]


def convList(submittedList):
    return [iter(dic[elem] for elem in tab) for tab in submittedList]
