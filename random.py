import random 
dist = []
row=40
col=35
for i in range(0, row):
    sublist = []
    for j in range(0,col):
        char=' '
        if (i==0 or j==0 or i==row-1 or j==col-1):
            char='x'
        sublist.append(char)
    dist.append(sublist)
wall=random.randint(50,100)
for i in range(0,wall):
    x=random.randint(1,row-1)
    y=random.randint(1,col-1)
    dist[x][y]='x'
with open('bonus3.txt', 'w') as outfile:
    bonus=0
    outfile.write(str(bonus))
    outfile.write('\n')
    for i in range(0,bonus):

        value=random.randint(-20,-1)
        x=random.randint(1,row-2)
        y=random.randint(1,col-2)
        outfile.write(str(x)+" "+str(y)+" "+str(value)+'\n')
        
        dist[x][y]='+'
    x=random.randint(1,row-1)
    y=random.randint(1,col-1)
    dist[x][y]='S'
    y=random.randint(1,col-1)
    dist[0][y]=' '
    bonus=4
    outfile.write(str(bonus))
    outfile.write('\n')
    for i in range(0,bonus):

        x=random.randint(1,row-2)
        y=random.randint(1,col-2)
        x1=random.randint(1,row-2)
        y1=random.randint(1,col-2)
        outfile.write(str(x)+" "+str(y)+" "+str(x1)+" "+str(y1)+'\n')
        
    print(dist)
    
    for i in range(0,row):
        for j in range(0,col):
            outfile.write(dist[i][j])
        outfile.write('\n')

