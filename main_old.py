import sys
sys.path.append('./models')
from course import Course
from daytime import Daytime
import re

file = open("courses.csv","r")
lines = file.readlines()
file.close()

temp = []
temp_day = []
course_list = []

def time_conv(time):
    try:
        x = time.split(":")
        #print(x)
        minute = int(x[1])
        hour = int(x[0])
        new_minute = (hour*60) + minute
        return new_minute
    except:
        pass
    

def day_time(data):
    time_range = list(map(time_conv,data)) 
    if time_range != [None]:
        x = Daytime(day,time_range[0],time_range[1])
        return x
    else:
        pass
file = open("text.txt","a+")
for line in lines:
    data = re.split(r',(?!\s)', line) #splits on comma, except for teacher name
    try:
        check = int(data[0][0]) #checks if first value is empty
        section = re.sub(r'0+[^1-9]',"",data[0][:5])
        if data[1] == "" or data[2] == "": #course number 
            number = data[0][5:].strip()
            if data[1] == "": #course name
                name = data[2]
            elif data[2] == "":
                name = data[1]
        elif len(data) < 6:
            number = data[0][5:].strip()
            name = data[1]
        else: #normal case
            number = data[1]
            name = data[2]

        for day in data[3]:
            times = data[-2].split("-")
            temp_day.append(day_time(times))

        temp.append(section)
        temp.append(number)
        temp.append(name)
    except:
        if re.search(r'\w+,\s\w+',data[2]): #teacher
            teacher = data[2]
            temp.append(teacher)
            temp.append(temp_day)
            file.write(str(temp))
            temp.clear() #clears temp lists
            temp_day.clear()
        if data[-2] == "":
            continue
        else:
            times = data[-2].split("-")
            temp_day.append(day_time(times))

temp.append(temp_day)
course_list.append(temp)

print(course_list)            

