import sys
sys.path.append('./models')
from course import Course
from daytime import Daytime
import re

def readFile(filename):
    file = open(filename,"r")
    lines = file.readlines()
    file.close()
    return lines

def time_conv(time):
    x = time.split(":")
    minute = int(x[1])
    hour = int(x[0])
    new_minute = (hour*60) + minute
    return new_minute

def day_time(day,time):
    time_range = list(map(time_conv,time))
    daytime_obj = Daytime(day,time_range[0],time_range[1])
    return daytime_obj

def new_course_check(line):
    if line[0] == '':
        return False
    else:
        return True

def find_teacher(data):
    if re.search(r'\w+,\s\w+',data[2]):
        teacher = data[2]
        return teacher

empty_list = {'section' : '',
             'number' : '',
             'name' : '',
             'teacher' : '',
             'daytimes' : []}

def make_course_list(filename):
    lines = readFile(filename)
    course_list = []
    temp = empty_list
    temp_day = []
    for line in lines:
        data = re.split(r',(?!\s|")', line.rstrip()) #splits on comma, except for teacher name
        if new_course_check(data) == True: #check if new course
            temp['daytimes'] = temp_day
            x = Course(temp['section'],temp['number'],temp['name'],temp['teacher'],temp['daytimes'])
            course_list.append(x)
            temp = empty_list #resets dict
            temp_day = []

            temp['section'] = data[0]
            temp['number'] = data[1]
            temp['name'] = data[2]
            days = data[3]
            time = data[4].split('-')
            for day in days:
                time_obj = day_time(day, time)
                temp_day.append(time_obj)
        else:
            teacher = find_teacher(data)
            if teacher != None:
                temp['teacher'] = teacher
            if data[3] != '':
                days = data[3]
                time = data[4].split('-')
                for day in days:
                    time_obj = day_time(day, time)
                    temp_day.append(time_obj)
                    
    x = Course(temp['section'],temp['number'],temp['name'],temp['teacher'],temp['daytimes'])
    course_list.append(x)
    course_list.pop(0)
    
    return course_list




