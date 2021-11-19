import sys
import numpy as np
from collections import defaultdict

def addEdge(graph,u,v):
    """
    Add edge from vertex u to v
    """
    graph[u].append(v)

def gengraph(remaze,r,c):
    """
    Generate the graph 
    - input: matrix that contains elements of the maze, number of rows and columns of the maze
    - output：graph that contains all nodes and edges
    """
    #initialize graph as dictionary
    graph = defaultdict(list)
    
    for i in range(r):
        for j in range(c):
            if (remaze[i][j][3] == 'N'):
                for k in range(0,i+1,1): #N: moving up, changing i, i-k>0
                    if (remaze[i-k][j][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i-k][j])
            elif (remaze[i][j][3] == 'S'):
                for k in range(0,r-i,1):#S: moving down, changing i, i+k<r-1
                    if (remaze[i+k][j][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i+k][j])
            elif (remaze[i][j][3] == 'W'):
                for k in range(0,j+1,1):#W: moving to the left, changing j, j-k>0
                    if (remaze[i][j-k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i][j-k])
            elif (remaze[i][j][3] == 'E'):
                for k in range(0,c-j,1):#E: moving to the right, changing j, j+k<c-1
                    if (remaze[i][j+k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i][j+k])
            elif (remaze[i][j][3] == 'NW'):
                for k in range(0,min(i+1,j+1),1):#NW: moving to the up-left, changing both i and j, i-k,j-k>0
                    if (remaze[i-k][j-k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i-k][j-k])
            elif (remaze[i][j][3] == 'SW'):
                for k in range(0,min(r-i,j+1),1):#SW: moving to the down-left, changing both i and j, j-k>0, i+k<r-1
                    if (remaze[i+k][j-k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i+k][j-k])
            elif (remaze[i][j][3] == 'NE'):
                for k in range(0,min(i+1,c-j),1):#NE: moving to the up-right, changing both i and j, i-k>0, j+k<c-1
                    if (remaze[i-k][j+k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i-k][j+k])
            elif (remaze[i][j][3] == 'SE'):
                for k in range(0,min(r-i,c-j),1):#SE: moving to the down-right, changing both i and j, i+k<r-1, j+k<c-1
                    if (remaze[i+k][j+k][2] != remaze[i][j][2]):
                        addEdge(graph,remaze[i][j],remaze[i+k][j+k])
            else:# if we already at the bullseye or trying to go out of range
                break            
    return graph

def dfspath(graph, start, end):
    """
    Finding path by dfs
    - input: the graph, start vertex(0,0), end vertex(bullseye)
    - output：Path
    """
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
    #replace O as O-O to match the format
    maze[r-1][c-1] = 'O-O'
    #initialize a rxc matrix remaze
    remaze = [ [0 for k in range(r)] for q in range(c)]
    #transfer elements from maze to remaze, with it's index, color and direction
    for i in range(r):
        for j in range(c):
            remaze[i][j] = (i,j, maze[i][j].split('-')[0], maze[i][j].split('-')[1])
    #getting the graph    
    G = gengraph(remaze,r,c)
    #getting the path
    P = dfspath(G, remaze[0][0], remaze[r-1][c-1])
    if P:#write only if a path is found
        #write path to the file
        w = open(otfile,'a')
        #clean the file before write
        w.truncate(0)
        for i in range(len(P)-1):
            #the distance is either dx!=0, dy=0; dx=0, dy!=0 or dx=dy!=0
            num = max(abs(P[i+1][0]-P[i][0]),abs(P[i+1][1]-P[i][1]))
            direc = P[i][3]
            w.write(str(num)+direc)
            w.write(' ')
        #close the output file
        w.close()
    else:#when there is no path found
        print('Path not found!')
