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
test_list = [iter(elem for elem in tab) for tab in x]


def generateTree(rootValue,courseList):
    global tree,currentCourse,previousNode,count, lst
    lst = courseList
    rootNode = Node(value=rootValue)
    tree = Tree(rootNode)
    count = tree.courseCount #starts at 1
    previousNode = rootNode #sets previous node to root to start
    # currentCourse = next(courseList[count])
    def recursiveGenerate():
        global tree,previousNode,count,lst
        temp = tree
        while count < len(lst):
            currentCourse = next(lst[count])
            x = tree.checkValid(currentCourse)
            if x:
                newNode = tree.createEdge(previousNode,currentCourse)
                count += 1
                previousNode = newNode
                recursiveGenerate()
            else:
                #currentCourse = next(lst[count])
                recursiveGenerate()

    recursiveGenerate()
    return tree
    
"""
sampleRootVal = next(test_list[0])
myTree = generateTree(sampleRootVal,test_list)
root = myTree.root
l1 = root.children[0]
l2 = l1.children[0]
l3 = l2.children[0]
l4 = l3.children[0]
l5 = l4.children[0]
l6 = l5.children[0]
x = [l1,l2,l3,l4,l5,l6]

for i in x:
    print(i.value.number)

"""