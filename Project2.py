import sys
import numpy as np
from collections import defaultdict

def addEdge(graph,u,v):
    graph[u].append(v)

def gengraph(remaze,r,c):
    graph = defaultdict(list)
    
    for i in range(r):
        for j in range(c):
            if (remaze[i][j][3] == 'N'):
                for k in range(0,i+1,1):
                    if (remaze[i-k][j][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i-k][j])
            elif (remaze[i][j][3] == 'S'):
                for k in range(0,r-i,1):
                    if (remaze[i+k][j][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i+k][j])
            elif (remaze[i][j][3] == 'W'):
                for k in range(0,j+1,1):
                    if (remaze[i][j-k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i][j-k])
            elif (remaze[i][j][3] == 'E'):
                for k in range(0,c-j,1):
                    if (remaze[i][j+k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i][j+k])
            elif (remaze[i][j][3] == 'NW'):
                for k in range(0,min(i+1,j+1),1):
                    if (remaze[i-k][j-k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i-k][j-k])
            elif (remaze[i][j][3] == 'SW'):
                for k in range(0,min(r-i,j+1),1):
                    if (remaze[i+k][j-k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i+k][j-k])
            elif (remaze[i][j][3] == 'NE'):
                for k in range(0,min(i+1,c-j),1):
                    if (remaze[i-k][j+k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i-k][j+k])
            elif (remaze[i][j][3] == 'SE'):
                for k in range(0,min(r-i,c-j),1):
                    if (remaze[i+k][j+k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i+k][j+k])
            else:# if we already at the bulleye or trying to go out of range
                break            
    return graph

def dfspath(graph, start, end):
    #add start vertex to the stack
    stack = [(start, [start])]
    visit = set()
    while stack:
        #get the vertex from stack
        (v, path) = stack.pop()
        if v not in visit:
            if v == end:
                #path found
                return path
            visit.add(v)
            #add its neighbors to the stack
            for ngb in graph[v]:
                stack.append((ngb, path + [ngb]))
                
                
#The program must take two command line parameters: (1) the input file name; and (2) the output file name.
infile = sys.argv[1]   #input file name
otfile = sys.argv[2]   #output file name
if __name__ == "__main__":
    content = open(infile,'r')
    #record number of rows and columns
    dim = content.readline()
    dim1 = dim.split()
    r = int(dim1[0])
    c = int(dim1[1])
    
   #read in the maze and store as a matrix
    with content as f:
         m = [[wor for wor in line.split()] for line in f]
    content.close() 
    maze = np.array(m)
    maze[r-1][c-1] = 'O-O'
    #initialize a rxc matrix remaze
    remaze = [ [0 for k in range(r)] for q in range(c)]
    #transfer elements from maze to remaze, with it's index, color and direction
    for i in range(r):
        for j in range(c):
            remaze[i][j] = (i,j, maze[i][j].split('-')[0], maze[i][j].split('-')[1])
        
    G = gengraph(remaze,r,c)
    
    P = dfspath(G, remaze[0][0], remaze[r-1][c-1])
    w = open(otfile,'a')
    w.truncate(0)
    for i in range(len(P)-1):
        num = max(abs(P[i+1][0]-P[i][0]),abs(P[i+1][1]-P[i][1]))
        direc = P[i][3]
        w.write(str(num)+direc)
        w.write(' ')
    w.close()   
