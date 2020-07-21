import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from os 
from random import randint

blockToIndex = {
    495: 0,
    525: 1,
    555: 2,
    585: 3,
    615: 4,
    645: 5,
    675: 6,
    705: 7,
    735: 8,
    765: 9,
    795: 10,
    825: 11,
    855: 12,
    885: 13,
    915: 14,
    945: 15,
    975: 16,
    1005: 17,
    1035: 18,
    1065: 19,
    1095: 20,
    1125: 21,
    1155: 22,
    1185: 23,
}

weekdays = {"M": 0, "T": 1, "W": 2, "H": 3, "F": 4, "S": 5}


 



def makeFolder(saveDir):
    unique = randint(1000)
    folderPath = f'{saveDir}/unique'
    return folderPath

def objToArray(courseList: list):
    arr = np.ndarray(size=(6, 24))  # create 6 by 24 grid
    arr.fill(0)  # set all values to 0
    count = 1
    courseCount = {}
    for course in courseList:
        daytime = course.daytimes
        for key in daytime:
            xIndex = weekdays[key]
            for block in daytime[key]:
                yIndex = blockToIndex[block]
                arr[yIndex][xIndex] = count
        courseCount[count] = course.number
        count += 1
    return arr, courseCount


def graphic(array, saveDir):
    plot = plt.pcolormesh(Z, cmap=plt.cm.get_cmap("Blues", 8))
    plt.colorbar(plot)
    plt.clim(-0.5, 8.5)
    plt.savefig(f"{saveDir}.png")


