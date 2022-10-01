""" ##########################################################
Breadth first search for the sliding puzzle
for INC491 Deep learning and Artificial Intelligence class
Dept. INC King Mongkut's Univ. Technology Thonburi KMUTT
By Poj Tangamchit & Pak Laowattanachai
###########################################################"""
import numpy as np
import random

####################    Node definitions   ###########################
class Node:
    def __init__(self, state, action, parent, cost):
        self.s = state
        self.a = action
        self.p = parent
        self.c = cost
        self.expand = 0

    def printstate(self):
        print(self.s)

    def printaction(self):
        print(self.a)

################## Action functions ##################################
def swap(array,p1,p2,p3,p4):
    temp=array[p1,p2]
    array[p1,p2]=array[p3,p4]
    array[p3,p4]=temp
    return array

def goup(value):
    value = np.array(value)
    a=(np.where(value==0))
    if a[0][0]-1<0:
        return value
    else:
        ans=swap(value,a[0][0],a[1][0],a[0][0]-1,a[1][0])
        return ans

def godown(value):
    value = np.array(value)
    a=(np.where(value==0))
    if a[0][0]+1==value.shape[1]:
        return value
    else:
        ans=swap(value,a[0][0],a[1][0],a[0][0]+1,a[1][0])
        return ans

def goleft(value):
    value = np.array(value)
    a=(np.where(value==0))
    if a[1][0]-1<0:
        return value
    else:
        ans=swap(value,a[0][0],a[1][0],a[0][0],a[1][0]-1)
        return ans

def goright(value):
    value = np.array(value)
    a=(np.where(value==0))
    if a[1][0]+1==value.shape[1]:
        return value
    else:
        ans=swap(value,a[0][0],a[1][0],a[0][0],a[1][0]+1)
        return ans

def get_minvalue(inputlist):
    #get the minimum value in the list
    min_value = min(inputlist)

    #return the index of minimum value
    min_index=[]
    for i in range(0,len(inputlist)):
      if min_value == inputlist[i]:
        min_index.append(i)

    return min_index

def heuristic_min(state1, state2, state3, state4, level, value, last_state):
    value = np.array(value)
    a=(np.where(value==0))
    heu1 = sum(sum(state1.s != goal)) + level # up
    heu2 = sum(sum(state2.s != goal)) + level # down
    heu3 = sum(sum(state3.s != goal)) + level # left
    heu4 = sum(sum(state4.s != goal)) + level # right

    ### cannot go back to last state ###
    # up
    if last_state == 0:
        heu2 = 99999 # cannot go down back
    # down
    if last_state == 1:
        heu1 = 99999 # cannot go up back
    # left
    if last_state == 2:
        heu4 = 99999 # cannot go right back
    # right
    if last_state == 3:
        heu3 = 99999 # cannot go left back

    ### check if it can reach the "edge"
    # up
    if a[0][0]-1<0:
        heu1 = 99999 # cannot go up more
    # down
    if a[0][0]+1==value.shape[1]:
        heu2 = 99999 # cannot go down more
    # left
    if a[1][0]-1<0:
        heu3 = 99999 # cannot go left more
    # right
    if a[1][0]+1==value.shape[1]:
        heu4 = 99999 # cannot go right more

    heus = [heu1, heu2, heu3, heu4]
    heu_min = get_minvalue(heus)
    min_index = random.choice(heu_min)
    return min_index

##########################   Main   #######################################
maxdepth = 9999
#start = np.array([[1,2,3],[4,5,6],[0,7,8]])  # change your starting here
# start = np.array([[4,1,0],[7,2,3],[5,8,6]])   # change your starting here
start = np.array([[4,1,3],[7,2,6],[5,8,0]])
goal = np.array([[1,2,3],[4,5,6],[7,8,0]])

root = Node(start,0,0,0)
nodelist = [root]
costlist = np.array([0])
nodecount = 1
last_state = None

found = None
while found==None:
    # Search for a node to expand [BREADTH FIRST]
    # breadth = np.argmin(costlist)
    # costlist[breadth] = maxdepth        # Eliminate found node from the list
    # parent = nodelist[breadth]

    # Search for a node to expand [A*]
    Astar = np.argmin(costlist)
    costlist[Astar] = maxdepth
    parent = nodelist[Astar]

    # Expand [BREADTH FIRST]
    # parent.expand = 1   # Mark expanded
    # depth = parent.c + 1
    # up = Node(goup(parent.s), 'up', parent, depth)
    # down = Node(godown(parent.s), 'down', parent, depth)
    # left = Node(goleft(parent.s), 'left', parent, depth)
    # right = Node(goright(parent.s), 'right', parent, depth)
    # nodelist.extend([up,down,left,right])
    # costlist = np.append(costlist,[depth,depth,depth,depth])

    # Expand [A*]
    parent.expand = 1   # Mark expanded
    depth = parent.c + 1
    up = Node(goup(parent.s), 'up', parent, depth)
    down = Node(godown(parent.s), 'down', parent, depth)
    left = Node(goleft(parent.s), 'left', parent, depth)
    right = Node(goright(parent.s), 'right', parent, depth)
    heu_index = heuristic_min(up, down, left, right, depth, parent.s, last_state)
    last_state = heu_index

    if heu_index == 0:
        nodelist.extend([up])
        print("up")
    elif heu_index == 1:
        nodelist.extend([down])
        print("down")
    elif heu_index == 2:
        nodelist.extend([left])
        print('left')
    elif heu_index == 3:
        nodelist.extend([right])
        print('right')

    costlist = np.append(costlist,[depth])

    # Check if a solution is found
    if sum(sum(up.s != goal)) == 0:
        found = up
    if sum(sum(down.s != goal)) == 0:
        found = down
    if sum(sum(left.s != goal)) == 0:
        found = left
    if sum(sum(right.s != goal)) == 0:
        found = right

    nodecount = nodecount + 4

# Print solution
print('Solution found in ' + str(found.c) + ' moves')
print('Generated ' + str(nodecount) + ' nodes')
solution = []
while found.c > 0 :
    solution.append(found)
    found = found.p

print(start)
for i in range(len(solution)-1,-1,-1):
    solution[i].printaction()
    solution[i].printstate()
