
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
def visualize_maze(matrix, bonus,dichchuyen, start, end, route=None,outputname='output.txt'):
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
                        marker=direction[i],color='blue')

    plt.text(end[1],-end[0],'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    colors=['yellow','orange','brown','pink','gray','black']
    index=0
    for item in dichchuyen:
        begin=item
        plt.scatter(begin[1],-begin[0],marker='d',s=100,color=colors[index%len(colors)])
        plt.scatter(dichchuyen[begin][1],-dichchuyen[begin][0],marker='d',s=100,color=colors[index%len(colors)])
        index+=1
    plt.xticks([])
    plt.yticks([])
    plt.savefig('./'+outputname+'/algo2.jpg')
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
  vtri_dichchuyen={}
  n_dich_chuyen = int(next(f)[:-1])
  for i in range(n_dich_chuyen):
    x, y, x1,y1 = map(int, next(f)[:-1].split(' '))
    vtri_dichchuyen[(x,y)]=(x1,y1)  
    vtri_dichchuyen[(x1,y1)]=(x,y) 
  text=f.read()
 
  matrix=[list(i) for i in text.splitlines()]
  for index,item in enumerate(vtri_dichchuyen):

    if (index%2==0):
        print(index,item)
        matrix[item[0]][item[1]]='D'
        matrix[vtri_dichchuyen[item][0]][vtri_dichchuyen[item][1]]='E'
  f.close()

  return bonus_points,mapbonus, matrix,vtri_dichchuyen



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
def add_index(list,dist,cost):
    i=0
    node=list[i]
    while dist[node.position[0]][node.position[1]]<cost:
        i+=1
        node=list[i]
    return i

def search(maze, cost, start, end,bonus,dich_chuyen,outputpath):
    
   
    start_node = Node(None, tuple(start))
    end_node = Node(None, tuple(end))
    yet_to_visit_list = []  
    visited_list = [] 
    yet_to_visit_list.append(start_node)
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
    while len(yet_to_visit_list) > 0:
        min_cost=INF
        current_index = len(yet_to_visit_list)-1  
        current_node = yet_to_visit_list[current_index]
        for i in yet_to_visit_list :
            if dist[i.position[0]][i.position[1]]<min_cost:
                min_cost=dist[i.position[0]][i.position[1]]
                current_node=i    
        yet_to_visit_list.remove(current_node)
        visited_list.append(current_node)
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
            # Create new node
            new_node = Node(current_node, node_position)
           
            # Appendp
            newNode.append(new_node)
        if maze[current_node.position[0]][current_node.position[1]]=='D':
            node_i=dich_chuyen[(current_node.position[0],current_node.position[1])]
            print(node_i)
            # if dist[node_i[0]][node_i[1]]<=dist[current_node.position[0]][current_node.position[1]]:
            #     continue
            new_node = Node(current_node, node_i)
            newNode=[new_node]
        for cur in newNode:
            if (maze[cur.position[0]][cur.position[1]] in [' ','+','D','E']):
                cost_maz=1
                if maze[cur.position[0]][cur.position[1]]=='D':
                    cost_maz=0
    
                if maze[cur.position[0]][cur.position[1]]=='+':
                    cost_maz=bonus[(cur.position[0],cur.position[1])]+1
                    maze[cur.position[0]][cur.position[1]]='-'
                
                if dist[current_node.position[0]][current_node.position[1]] +cost_maz < dist[cur.position[0]][cur.position[1]] :
    
                    for i in yet_to_visit_list :
                        if cur.position == i.position:
                            yet_to_visit_list.remove(i)
                   
                    dist[cur.position[0]][cur.position[1]]=dist[current_node.position[0]][current_node.position[1]] + cost_maz
                    yet_to_visit_list.append(cur)
    if chiphi==INF:
        with open('./'+outputpath+'/algo2.txt', 'w') as outfile:
            outfile.write('NO')
            outfile.close
            return []
    return return_path(try_node,chiphi,outputpath)
            
def algo2(name,outputname):
    bonus_points,mapbonus, matrix ,vtri_dichchuyen= read_file(name)


    print(vtri_dichchuyen)
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


    answer= search(matrix,cost, start, end,mapbonus,vtri_dichchuyen,outputname)

    visualize_maze(matrix,bonus_points,vtri_dichchuyen,start,end,answer,outputname)
# start_time=time.time()
# dichchuyen('maze_dichchuyen.txt')
# end_time=time.time()
# print('thoi gian:',end_time-start_time)
# bonus_points,mapbonus, matrix ,vtri_dichchuyen= read_file('maze_dichchuyen.txt')
# print(vtri_dichchuyen)
