""" ##########################################################
Breadth first search for the sliding puzzle
for INC491 Deep learning and Artificial Intelligence class
Dept. INC King Mongkut's Univ. Technology Thonburi KMUTT
By Poj Tangamchit & Pak Laowattanachai
###########################################################""" 
import numpy as np
    
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


##########################   Main   #######################################
maxdepth = 9999
#start = np.array([[1,2,3],[4,5,6],[0,7,8]])  # change your starting here
# start = np.array([[4,1,0],[7,2,3],[5,8,6]])   # change your starting here
start = np.array([[4,1,3],[7,2,0],[5,8,6]])
goal = np.array([[1,2,3],[4,5,6],[7,8,0]])

root = Node(start,0,0,0)
nodelist = [root]
costlist = np.array([0])
nodecount = 1

found = None
while found==None:
    # Search for a node to expand
    breadth = np.argmin(costlist)
    costlist[breadth] = maxdepth        # Eliminate found node from the list
    parent = nodelist[breadth]
        
    # Expand
    parent.expand = 1   # Mark expanded
    depth = parent.c + 1
    up = Node(goup(parent.s), 'up', parent, depth)
    down = Node(godown(parent.s), 'down', parent, depth)
    left = Node(goleft(parent.s), 'left', parent, depth)
    right = Node(goright(parent.s), 'right', parent, depth)
    nodelist.extend([up,down,left,right])
    costlist = np.append(costlist,[depth,depth,depth,depth])
    
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
    