import time

import os
import re
from turtle import end_fill
import matplotlib.pyplot as plt
from numpy import append
from cmath import sqrt
from sqlite3 import Row
import numpy as np
import math
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
                marker='P',s=100,color='green')

    plt.scatter(start[1],-start[0],marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='blue')

    plt.text(end[1],-end[0],'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('./'+outputname+'/algo1.jpg')
    plt.close()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
    
    for _, point in enumerate(bonus):
      print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

def read_file(file_name: str = 'mazetrix.txt'):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  mapbonus={}
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))
    mapbonus[(x,y)]=reward

  print('bn:',bonus_points)
  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()

  return bonus_points,mapbonus, matrix



cost=1

e=1.5
INF=100000
class Node:


    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
    def __eq__(self, other):
        return self.position == other.position

def return_path(current_node,chiphi,outputpath):
    path = []
   
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    with open('./'+outputpath+'/algo.txt', 'w') as outfile:
       outfile.write(str(chiphi))
       outfile.close()
    path = path[::-1]
    return path

def search(maze, cost, start, end,bonus,outputpath):
    
   
    start_node = Node(None, tuple(start))
    end_node = Node(None, tuple(end))
    open = []  
    close = [] 
    open.append(start_node)
    try_node=end_node
    chiphi=INF

    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ]] # go right
 
    no_rows, no_columns = np.shape(maze)
    
    dist = []
    for i in range(0, len(maze)):
        sublist = []
        for j in range(0,len(maze[0])):
            sublist.append(INF)
        dist.append(sublist)
    dist[start[0]][start[1]]=0
    cost=0
    while len(open) > 0:
        min_cost=INF
        cost+=1
        current_index = len(open)-1  
        current_node = open[current_index]
        for i in open :
            if dist[i.position[0]][i.position[1]]<min_cost:
                min_cost=dist[i.position[0]][i.position[1]]
                current_node=i    

        open.remove(current_node)
        
        close.append(current_node)
        if current_node==end_node and dist[current_node.position[0]][current_node.position[1]]<chiphi:
            try_node=current_node
            chiphi=dist[current_node.position[0]][current_node.position[1]]
           
        newNode = []
        for new_position in move: 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (no_columns -1) or 
                node_position[1] < 0):
                continue
           
            if maze[node_position[0]][node_position[1]] =='x':
                continue
            new_node = Node(current_node, node_position)
            newNode.append(new_node)
        for child in newNode:
            if (maze[child.position[0]][child.position[1]] in [' ','+']):
                cost_maz=1
                if maze[child.position[0]][child.position[1]]=='+':
                    cost_maz=bonus[(child.position[0],child.position[1])]+1
                    maze[child.position[0]][child.position[1]]='-'
                if dist[current_node.position[0]][current_node.position[1]] +cost_maz < dist[child.position[0]][child.position[1]] :
                    for i in open :
                        if child == i:
                            open.remove(i)
                   
                    dist[child.position[0]][child.position[1]]=dist[current_node.position[0]][current_node.position[1]] + cost_maz
                    open.append(child)
    print('chi phi out code:',cost)
    if chiphi==INF:
        with open('./'+outputpath+'/algo1.txt', 'w') as outfile:
            outfile.write('NO')
            outfile.close
            return []
    return return_path(try_node,chiphi,outputpath)
def algo1(name,outputname):
    bonus_points,mapbonus, matrix = read_file(name)
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


    answer= search(matrix,cost, start, end,mapbonus,outputname)

    visualize_maze(matrix,bonus_points,start,end,answer,outputname)

