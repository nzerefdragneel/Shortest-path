
import os
import re
from turtle import end_fill
import matplotlib.pyplot as plt
from numpy import append
import numpy as np
import time
def visualize_maze(matrix, bonus, start, end, route=None,outputname='output.txt'):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v') #^
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^') #v        
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')
        

        

    #2. Drawing the map
    ax=plt.figure(dpi=100).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=50,color='black')
    
    plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                marker='P',s=50,color='green')

    plt.scatter(start[1],-start[0],marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='silver')

    plt.text(end[1],-end[0],'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('./'+outputname+'/astar.jpg')
    plt.close()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
    
    for _, point in enumerate(bonus):
      print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

def read_file(file_name: str = 'maze.txt'):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
 
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))
   
  print('bn:',bonus_points)
  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()

  return bonus_points, matrix



cost=1

e=1.5

class Node:
   
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 1
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

def return_path(current_node,outputpath):
    path = []
    current = current_node
    chiphi=0
    while current is not None:
        chiphi+=1
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    print('./'+outputpath+'/astar.txt', 'w')
    with open('./'+outputpath+'/astar.txt', 'w') as outfile:
       outfile.write(str(chiphi-1))
       outfile.close()
    return path


def search(maze, cost, start, end,outputpath):
    

    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    
    list_open = []  
    close = [] 
    list_open.append(start_node)
    cost = 0
    max_code = (len(maze) // 2) ** 10

    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ]] # go right


  
    no_rows, no_columns = np.shape(maze)
    while len(list_open) > 0:
        cost += 1    
        current_node = list_open[0]
        current_index = 0
        for index, item in enumerate(list_open):
            if item.f < current_node.f:
                current_node = item
                current_index = index     
        if cost > max_code:
            with open('./'+outputpath+'/astar.txt', 'w') as outfile:
                outfile.write('NO')
                outfile.close()
            return return_path(current_node,outputpath)
        list_open.pop(current_index)
        close.append(current_node)
        if current_node == end_node:
            print('Chi phi out code:',cost)
            
            return return_path(current_node,outputpath)
        newNode = []

        for cur in move: 
            node_position = (current_node.position[0] + cur[0], current_node.position[1] + cur[1])
            if (node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (no_columns -1) or 
                node_position[1] < 0):
                continue
            if maze[node_position[0]][node_position[1]] =='x':
                continue
            new_node = Node(current_node, node_position)
            newNode.append(new_node)
        for cur in newNode:
            if len([visited_cur for visited_cur in close if visited_cur.position == cur.position]) > 0:
                continue
            cur.g = current_node.g + cost
            # cur.h = (((cur.position[0] - end_node.position[0]) ** 2) + 
            #            ((cur.position[1] - end_node.position[1]) ** 2)) 
            # cur.h=e*current_node.h
            cur.h = ((abs(cur.position[0] - end_node.position[0])) + 
                       (abs(cur.position[1] - end_node.position[1]))) **2
            cur.f = cur.g + cur.h
            if len([i for i in list_open if cur == i and cur.g > i.g]) > 0:
                continue
            list_open.append(cur)
    with open('./'+outputpath+'/astar.txt', 'w') as outfile:
                outfile.write('NO')
                outfile.close()
    return []


def astar(name,outputname):
    bonus_points, matrix = read_file(name)

    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j]=='S':
                start=(i,j)

            elif matrix[i][j]==' ':
                if (i==0) or (i==len(matrix)-1) or (j==0) or (j==len(matrix[0])-1):
                    end=(i,j)
                    
            else:
                pass

    answer= search(matrix,cost, start, end,outputname)


    visualize_maze(matrix,bonus_points,start,end,answer,outputname)
# star_time=time.time()
# astar('bonus3.txt')
# end_time=time.time()
# print(end_time-star_time)