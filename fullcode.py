import dfs
import bfs
import ucs
import gbfs
import astar
import algo1
import algo2
# import mapcodiemcong
import os



main_dir = ["Output"] 
common_dir = ["level_1", "level_2", "advance"]
file=[]
for dir1 in main_dir:
    for dir2 in common_dir:
        try: os.makedirs(os.path.join(dir1,dir2))
        except OSError: pass
# chạy code  lv1: không có điểm thưởng

file=os.listdir(os.path.join('input',common_dir[0]))
listAlgorithm=['bfs','dfs','gbfs','astar','ucs']
for name in file:
    sub=name[0:name.find('.')]
    dir1='output/level_1/'
    inputname="input/level_1/"+name
    # bfs
    print('BFS:')    
    dir2=sub+'/bfs'
    path_bfs=os.path.join(dir1,dir2)
    try: os.makedirs(path_bfs)
    except OSError: pass
    bfs.bfs(inputname,path_bfs)
    #dfs
    print('DFS:')    
    dir2=sub+'/dfs'
    path_dfs=os.path.join(dir1,dir2)
    try: os.makedirs(path_dfs)
    except OSError: pass
    dfs.dfs(inputname,path_dfs)
    # ufs
    print('UCS:')    
    dir2=sub+'/ucs'
    path_ucs=os.path.join(dir1,dir2)
    try: os.makedirs(path_ucs)
    except OSError: pass
    ucs.ucs(inputname,path_ucs)
    #gbfs
    print('GBFS:')    
    dir2=sub+'/gbfs'
    path_gbfs=os.path.join(dir1,dir2)
    try: os.makedirs(path_gbfs)
    except OSError: pass

    gbfs.gbfs(inputname,path_gbfs)
    #astar
    print('ASTAR:')    
    dir2=sub+'/astar'
    path_astar=os.path.join(dir1,dir2)
    try: os.makedirs(path_astar)
    except OSError: pass
    astar.astar(inputname,path_astar)
file=os.listdir(os.path.join('input',common_dir[1]))

for name in file:
    sub=name[0:name.find('.')]
    dir1='output/level_2/'
    inputname="input/level_2/"+name
    print('ALGO 1:')    
    dir2=sub+'/algo1'
    path_algo1=os.path.join(dir1,dir2)
    try: os.makedirs(path_algo1)
    except OSError: pass
    algo1.algo1(inputname,path_algo1)
file=os.listdir(os.path.join('input',common_dir[2]))

for name in file:
    sub=name[0:name.find('.')]
    dir1='output/advance/'
    inputname="input/advance/"+name
    print('ALGO 2:')    
    dir2=sub+'/algo2'
    path_algo2=os.path.join(dir1,dir2)
    try: os.makedirs(path_algo2)
    except OSError: pass
    algo2.algo2(inputname,path_algo2)


