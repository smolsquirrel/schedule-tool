import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from math import floor
import sys

sys.path.append("./models")
from course import Course



def makeFolder(saveDir):
    unique = randint(1000, 9999)
    folderPath = f"{saveDir}/{unique}"
    return folderPath


def objToArray(courseList: list):
    arr = np.ndarray(shape=(24, 6))  # create 6 by 24 grid
    arr.fill(1)  # set all values to 0

    # set activity periods
    for row in [12, 13, 14]:
        for column in [1, 3]:
            arr[row][column] = 9

    count = 2
    courseOrder = []
    for course in courseList:
        daytime = course.daytimes
        for key in daytime:
            xIndex = weekdays[key]
            for block in daytime[key]:
                yIndex = blockToIndex[block]
                arr[yIndex][xIndex] = count
        courseOrder.append(course.number)
        count += 1
    courseOrder.append("Activity Period")
    return arr, courseOrder  # , courseCount


def graphic(array, courseOrder, saveDir):
    unique = randint(1000, 9999)
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    fig.set_figheight(12)

    colors = [
        (255 / 255, 255 / 255, 255 / 255),  # rgb(255, 255, 255)
        (238 / 255, 82 / 255, 83 / 255),  # rgb(238, 82, 83)
        (10 / 255, 189 / 255, 227 / 255),  # rgb(10, 189, 227)
        (16 / 255, 172 / 255, 132 / 255),  # rgb(16, 172, 132)
        (255 / 255, 159 / 255, 67 / 255),  # rgb(255, 159, 67)
        (95 / 255, 39 / 255, 205 / 255),  # rgb(95, 39, 205)
        (46 / 255, 134 / 255, 222 / 255),  # rgb(46, 134, 222)
        (243 / 255, 104 / 255, 224 / 255),  # rgb(243, 104, 224)
        (0 / 255, 210 / 255, 211 / 255),  # rgb(0, 210, 211)
    ]
    cMap = matplotlib.colors.LinearSegmentedColormap.from_list("a", colors, N=9)
    bounds = np.arange(0.5, 9.5, 1)
    norm = matplotlib.colors.Normalize(vmin=0.5, vmax=9.5)
    cax = ax.pcolormesh(array, cmap=cMap, edgecolor="#000000", linewidth=0.5, norm=norm)
    cbar = fig.colorbar(cax)

    cbar.set_ticks(range(1, 10))
    courseOrder.insert(0, "None")  # add None to start of list
    cbar.set_ticklabels(courseOrder)

    ax.xaxis.tick_top()
    ax.set_xticks([float(tick - 0.5) for tick in range(1, 7)])
    ax.set_xticklabels(weekdays.keys())

    ax.set_yticks([float(tick + 0.5) for tick in range(0, 24)])
    ax.set_yticklabels(fullBlocksR)

    plt.show()

    plt.savefig(f"{saveDir}/{unique}.png")


blockToIndex = {
    495: 23,
    525: 22,
    555: 21,
    585: 20,
    615: 19,
    645: 18,
    675: 17,
    705: 16,
    735: 15,
    765: 14,
    795: 13,
    825: 12,
    855: 11,
    885: 10,
    915: 9,
    945: 8,
    975: 7,
    1005: 6,
    1035: 5,
    1065: 4,
    1095: 3,
    1125: 2,
    1155: 1,
    1185: 0,
}

weekdays = {"M": 0, "T": 1, "W": 2, "H": 3, "F": 4, "S": 5}


fullBlocksR = [
    "19:45-20:15",
    "19:15-19:45",
    "18:45-19:15",
    "18:15-18:45",
    "17:45-18:15",
    "17:15-17:45",
    "16:45-17:15",
    "16:15-16:45",
    "15:45-16:15",
    "15:15-15:45",
    "14:45-15:15",
    "14:15-14:45",
    "13:45-14:15",
    "13:15-13:45",
    "12:45-13:15",
    "12:15-12:45",
    "11:45-12:15",
    "11:15-11:45",
    "10:45-11:15",
    "10:15-10:45",
    "9:45-10:15",
    "9:15-9:45",
    "8:45-9:15",
    "8:15-8:45",
]
