import pickle
class Node:
    def __init__(self,value,parent=None):
        self.children = []
        self.parent = parent
        self.value = value

class Tree:
    def __init__(self,root : Node):
        self.root = root
        self.courseCount = 1
        self.availability = {
            'M' : {},
            'T' : {},
            'W' : {},
            'H' : {},
            'F' : {},
            'S' : {},
        }

    def createEdge(self, startingNode, endingValue):
        newNode = Node(parent=startingNode,value=endingValue)
        startingNode.children.append(newNode)
        return newNode

    def checkValid(self, course):
        daytimes = course.daytimes
        for key in daytimes: #day
            for block in daytimes[key]: #time block
                if block in self.availability[key]: #if time block is taken/unavailable in that day
                    return False
                else:
                    self.availability[key][block] = course.number
        return True

"""
           a
          / \
         b   c
        / \
       d   e
"""
x = pickle.load(open("save.p", "rb"))
x2 = pickle.load(open("save2.p", "rb"))
x3 = pickle.load(open("save3.p", "rb"))
test_list = [iter(elem for elem in tab) for tab in x]
test_list2 = [iter(elem for elem in tab) for tab in x2]
test_list3 = [iter(elem for elem in tab) for tab in x3]


def generateTree(rootValue,courseList):
    global tree,currentCourse,previousNode,count,lst, maxCount
    lst = courseList
    rootNode = Node(value=rootValue)
    tree = Tree(rootNode)
    count = tree.courseCount #starts at 1
    previousNode = rootNode #sets previous node to root to start
    maxCount = 1
    result = recursiveGenerate()
    if result == 0:
        return tree
    else:
        return False
    
def recursiveGenerate():
    global tree,previousNode,count,lst,maxCount
    if 0 < count:
        pass
    else:
        if maxCount != 7:
            return 1
        return 0
    try:
        currentCourse = next(lst[count])
    except (StopIteration, IndexError):
        count -= 1
        recursiveGenerate()
    checkResult = tree.checkValid(currentCourse)
    if checkResult:
        newNode = tree.createEdge(previousNode,currentCourse)
        count += 1
        if count > maxCount: #checks if atleast one valid tree
            maxCount = count
        previousNode = newNode
        recursiveGenerate()
    else:
        recursiveGenerate()


# 1 GER - ITA
# 2 GER
# 3 GER - ITA - ITA
# for i in test_list:
#     for j in i:
#         print(j.number)
sampleRootVal = next(test_list[0])
myTree = generateTree(sampleRootVal,test_list)



if myTree:
    try:
        l1 = root.children[0]
        l2 = l1.children[0]
        l3 = l2.children[0]
        l4 = l3.children[0]
        l5 = l4.children[0]
        l6 = l5.children[0]
        x = [l1,l2,l3,l4,l5,l6]

        for i in x:
            print(i.value.number)
    except:
        pass
else:
    print('failed')
