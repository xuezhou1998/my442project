############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Xuezhou Wen"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
from itertools import combinations, permutations
from collections import deque

import random
import queue
from queue import Queue
import copy
############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    return (math.factorial(n**2))/(math.factorial(n**2-n))

def num_placements_one_per_row(n):
    return n**n



def n_queens_valid(board):
    if board==[]:
        return True

    l=len(board)
    ##num_of_rows=max(max(board),len(board))
    newlist=deque()
    newboard1=deque(board)
    newboard=deque(board)
    for x in range(l):
        newlist.append([x,newboard1.pop()])
                
    for x in range(l):
        newboard.pop()
        if newlist[x][1] in newboard:
            ##print('1')
            return False
        for y in range(x+1,l):
            if abs(newlist[y][0]-newlist[x][0])==abs(newlist[y][1]-newlist[x][1]):
                
                return False
    return True

    





def n_queens_solutions(n):
    size=n
    q=deque()

    #initial q
    q.append([-1])

    while len(q)!=0:
        #print(q)
        c=q.popleft()
        #print(c)
        if c==[-1]:
            #print("1")
            for i in range(n):
                k=[]
                k.append(i)
                if n_queens_valid(k)==True:
                    q.appendleft(k)


        elif len(c)==size:
            #print("2")
            #if n_queens_valid(c)==True:
            yield c


        else:
            #print("3")
        #if n_queens_valid(c)==True:
            
            for i in range(n):
                k=copy.deepcopy(c)

                #print("ssss",k)
                k.append(i)
                if n_queens_valid(k)==True:
                    q.appendleft(k)

    return




            
    

def n_queens_helper(n,board):

##your board is keep changing it size and value!!!
    pass
        

           
        
     







############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        #self.row=row
        #self.col=col
        self.board=board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        if len(self.board)==0:
            return
        self.board[row][col]=not self.board[row][col]
        if row==0:
            self.board[row+1][col]=not self.board[row+1][col]
            if col==0:
                self.board[row][col+1]=not self.board[row][col+1]
            elif col==len(self.board[0])-1:
                self.board[row][col-1]=not self.board[row][col-1]

            elif 0<col<len(self.board[0])-1:
                self.board[row][col+1]=not self.board[row][col+1]
                self.board[row][col-1]=not self.board[row][col-1]

        elif row==len(self.board)-1:
            self.board[row-1][col]=not self.board[row-1][col]
            if col==0:
                self.board[row][col+1]=not self.board[row][col+1]
            elif col==len(self.board[0])-1:
                self.board[row][col-1]=not self.board[row][col-1]

            elif 0<col<len(self.board[0])-1:
                self.board[row][col+1]=not self.board[row][col+1]
                self.board[row][col-1]=not self.board[row][col-1]

        elif 0<row<len(self.board)-1:
            self.board[row+1][col]=not self.board[row+1][col]
            self.board[row-1][col]=not self.board[row-1][col]
            if col==0:
                self.board[row][col+1]=not self.board[row][col+1]
            elif col==len(self.board[0])-1:
                self.board[row][col-1]=not self.board[row][col-1]

            elif 0<col<len(self.board[0])-1:
                self.board[row][col+1]=not self.board[row][col+1]
                self.board[row][col-1]=not self.board[row][col-1]




    def scramble(self):
        rows=len(self.board)
        cols=len(self.board[0])
        for x in range(rows):
            for y in range(cols):
                result=random.random()<0.5
                #print(result)
                if result==True:
                    #print("1")
                    self.perform_move(x,y)





    def is_solved(self):
        rows=len(self.board)
        cols=len(self.board[0])
        for x in range(rows):
            for y in range(cols):
                if self.board[x][y]==True:
                    return False
        return True

    def copy(self):
        newboard=[]
        rows=len(self.board)
        cols=len(self.board[0])
        for x in range(rows):
            newboard.append([])
            for y in range(cols):
                newboard[x].append(self.board[x][y])

        return LightsOutPuzzle(newboard)

    def successors(self):
        
        rows=len(self.board)
        cols=len(self.board[0])
        for x in range(rows):
            for y in range(cols):
                p2=self.copy()
                a=tuple([x,y])
                p2.perform_move(x,y)
                #print(self.board)
                
                yield tuple([a,p2])

    def find_solution(self):
        rows=len(self.board)
        cols=len(self.board[0])
        size=rows*cols
        q=Queue()
        q.put(tuple([self.board,-1]))
        visited=[((-1,-1),-1)]
        sameboard=set()
        path=deque()
        indexx=-1
        path_final=deque()
        while q.empty()==False:
            indexx+=1
            qget=q.get()
            newlight,parent=LightsOutPuzzle(qget[0]),qget[1]
            if parent==-1:
                for move, new_p in newlight.successors():
                    tuplelist=[]
                    for i in range(rows):
                        
                        tuplelist.append(tuple(new_p.get_board()[i]))

                    tuple_board=tuple(tuplelist)
                    if tuple_board not in sameboard:
                        visited.append(tuple([move,indexx]))###not sure it should be placed outside the branch
                        q.put(tuple([new_p.get_board(),indexx]))

                        sameboard.add(tuple_board)

            
            elif newlight.is_solved()==True:
                    ##compute the path using parents! parent->parent's parent->parent's parent's parent...
                    ##initialize and update the path with the shortest one
                
                item=visited[indexx]
                path.appendleft(item[0])
                prev=item[1]
                while True:
                    if prev==-1:
                        break
                    item=visited[prev]
                    path.appendleft(item[0])
                    prev=item[1]
                    




                if len(path_final)==0:
                        ##initialize
                    path_final=copy.deepcopy(path)



                else:
                    if len(path)<len(path_final):
                        ##update
                        path_final=copy.deepcopy(path)
            else:
                for move, new_p in newlight.successors():
                    tuplelist=[]
                    for i in range(rows):
                        
                        tuplelist.append(tuple(new_p.get_board()[i]))

                    tuple_board=tuple(tuplelist)
                    if tuple_board not in sameboard:
                        visited.append(tuple([move,indexx]))###not sure it should be placed outside the branch
                        q.put(tuple([new_p.get_board(),indexx]))

                        sameboard.add(tuple_board)
        ##if len(path_final)==1:
            #return None 
        ##elif (-1,-1) in path_final:
        final=list(path_final)
        if (-1,-1) in final:
            final.remove((-1,-1))
        if final==[]:
            return None

        return final






        

def create_puzzle(rows, cols):
    newlist=[]
    for x in range(rows):
        a=[]
        newlist.append(a)
        for y in range(cols):
            newlist[x].append(False)
    

            
    return LightsOutPuzzle(newlist)


############################################################
# Section 3: Linear Disk Movement
############################################################
def disk_successors(Disk):
    
    newD=copy.deepcopy(Disk)
    
    for i in range(len(Disk)-1):

        if newD[i]==True:

            #print('1')
            #for j in range(2):
                #print(newD)
            if newD[i+1]==True and i+1<len(Disk)-1:
                if newD[i+2]==False:
                    newD2=copy.deepcopy(newD)
                    
                    

                    newD2[i]=False
                    newD2[i+1+1]=True
                    #print("s",newD2,i,i+1+1)
                    yield tuple([(i,i+1+1),newD2])
            elif newD[i+1]==False:
                newD2=copy.deepcopy(newD)
                
                

                newD2[i]=False
                newD2[i+1]=True
                #print("s",newD2,i,i+1)
                yield tuple([(i,i+1),newD2])
def disk_successors_distinct(Disk):

    newD=copy.deepcopy(Disk)
    
    for i in range(len(Disk)):

        if newD[i]!=-1:

            #print('1')
            #for j in range(2):
                #print(newD)
            for j in range(2):
                if j==0 and i<len(Disk)-1:#left
                    if newD[i+1]!=-1 and i+1<len(Disk)-1:
                        if newD[i+2]==-1:
                            newD2=copy.deepcopy(newD)
                            
                            

                            newD2[i]=-1
                            newD2[i+1+1]=newD[i]
                            #print("n",newD)
                            #print("s",newD2,i,i+1)

                            #print("s",newD2,i,i+1+1)
                            yield tuple([(i,i+1+1),newD2])
                    elif newD[i+1]==-1:
                        newD2=copy.deepcopy(newD)
                        
                        

                        newD2[i]=-1
                        newD2[i+1]=newD[i]
                        #print("n",newD)
                        #print("s",newD2,i,i+1)

                        yield tuple([(i,i+1),newD2])
                elif i>0:#right
                    if newD[i-1]!=-1 and i-1>0:
                        if newD[i-2]==-1:
                            newD2=copy.deepcopy(newD)
                            
                            

                            newD2[i]=-1
                            newD2[i-1-1]=newD[i]
                            #print("s",newD2,i,i+1+1)
                            

                            yield tuple([(i,i-1-1),newD2])
                    elif newD[i-1]==-1:
                        newD2=copy.deepcopy(newD)
                        
                        

                        newD2[i]=-1
                        newD2[i-1]=newD[i]
                        #print("s",newD2,i,i+1)
                        #print("n",newD)
                        #print("s",newD2,i,i+1)

                        yield tuple([(i,i-1),newD2])
    






def is_solved_identical(Disk):
    counter=0
    for i in reversed(Disk):
        if i==True:
            counter+=1
        else:
            break

    if counter==Disk.count(True):
        return True
    else:
        return False
def is_solved_distinct(Disk):
    if is_done_distinct(Disk)==False:
        return False

    counter=0
    for i in reversed(Disk):
        if i==counter:
            counter+=1
        else:
            break

    if counter==len(Disk)-Disk.count(-1):
        return True
    else:
        return False
    

def is_done_distinct(Disk):
    counter=0
    for i in reversed(Disk):
        if i!=-1:
            counter+=1
        else:
            break

    if counter==len(Disk)-Disk.count(-1):
        return True
    else:
        return False
    

def solve_identical_disks(length, n):

    origenal_borad=[]
    for i in range(length):
        if i<n:
            origenal_borad.append(True)
        else:
            origenal_borad.append(False)


    rows=length
    #cols=len(self.board[0])
    #size=rows*cols
    q=Queue()
    q.put(tuple([origenal_borad,-1]))
    visited=[((-1,-1),-1)]
    sameboard=set()
    path=deque()
    indexx=-1
    path_final=deque()
    while q.empty()==False:
        #print(visited)
        #print(list(q))
        indexx+=1
        #print(indexx)
        qget=q.get()
        #print(qget)
        newdisk,parent=qget[0],qget[1]
        if parent==-1:
            #print(newdisk)
            for move, new_p in disk_successors(newdisk):
                #print(new_p)
                #tuplelist=[]
                #for i in range(rows):
                    
                    #tuplelist.append(tuple(new_p[i]))

                tuple_board=tuple(new_p)
                if tuple_board not in sameboard:
                    visited.append(tuple([move,indexx]))###not sure it should be placed outside the branch
                    q.put(tuple([new_p,indexx]))

                    sameboard.add(tuple_board)

        
        elif is_solved_identical(newdisk)==True:
            #print(newdisk)
                ##compute the path using parents! parent->parent's parent->parent's parent's parent...
                ##initialize and update the path with the shortest one
            
            item=visited[indexx]
            path.appendleft(item[0])
            prev=item[1]
            while True:
                if prev==-1:
                    break
                item=visited[prev]
                path.appendleft(item[0])
                prev=item[1]
                



            #print(path)
            if len(path_final)==0:
                    ##initialize
                path_final=copy.deepcopy(path)
                #print('1')



            else:
                if len(path)<len(path_final):
                    print('2')
                    ##update
                    path_final=copy.deepcopy(path)
        #elif is_done_distinct(newdisk)==True:
         #   pass
        else:
            for move, new_p in disk_successors(newdisk):
                
                tuple_board=tuple(new_p)
                if tuple_board not in sameboard:
                    visited.append(tuple([move,indexx]))###not sure it should be placed outside the branch
                    q.put(tuple([new_p,indexx]))

                    sameboard.add(tuple_board)
    ##if len(path_final)==1:
        #return None 
    ##elif (-1,-1) in path_final:
    #final=reversed(list(path_final))
    final2=list(filter(lambda x: x!=(-1,-1),path_final))
    if final2==[]:
        return None

    return final2


def solve_distinct_disks(length, n):

    origenal_borad=[]
    for i in range(length):
        if i<n:
            origenal_borad.append(i)
        else:
            origenal_borad.append(-1)


    rows=length
    #cols=len(self.board[0])
    #size=rows*cols
    q=Queue()
    q.put(tuple([origenal_borad,-1]))
    visited=[((-1,-1),-1)]
    sameboard=set()
    path=deque()
    indexx=-1
    path_final=deque()
    while q.empty()==False:
        #print(visited)
        #print(list(q))
        indexx+=1
        #print(indexx)
        qget=q.get()
        #print(qget)
        newdisk,parent=qget[0],qget[1]
        if parent==-1:
            #print(newdisk)
            for move, new_p in disk_successors_distinct(newdisk):
                #print(new_p)
                #tuplelist=[]
                #for i in range(rows):
                    
                    #tuplelist.append(tuple(new_p[i]))

                tuple_board=tuple(new_p)
                if tuple_board not in sameboard:
                    visited.append(tuple([move,indexx]))###not sure it should be placed outside the branch
                    q.put(tuple([new_p,indexx]))

                    sameboard.add(tuple_board)

        
        elif is_solved_distinct(newdisk)==True:
            #print(newdisk)
                ##compute the path using parents! parent->parent's parent->parent's parent's parent...
                ##initialize and update the path with the shortest one
            
            item=visited[indexx]
            path.appendleft(item[0])
            prev=item[1]
            while True:
                if prev==-1:
                    break
                item=visited[prev]
                path.appendleft(item[0])
                prev=item[1]
                



            #print(path)
            if len(path_final)==0:
                    ##initialize
                path_final=copy.deepcopy(path)
                #print('1')



            else:
                if len(path)<len(path_final):
                    print('2')
                    ##update
                    path_final=copy.deepcopy(path)
        else:
            for move, new_p in disk_successors_distinct(newdisk):
                
                tuple_board=tuple(new_p)
                if tuple_board not in sameboard:
                    visited.append(tuple([move,indexx]))###not sure it should be placed outside the branch
                    q.put(tuple([new_p,indexx]))

                    sameboard.add(tuple_board)
    ##if len(path_final)==1:
        #return None 
    ##elif (-1,-1) in path_final:
    #final=reversed(list(path_final))
    final2=list(filter(lambda x: x!=(-1,-1),path_final))
    if final2==[]:
        return None

    return final2

    

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
20 hours
"""

feedback_question_2 = """
implementing the bfs algorithm
"""

feedback_question_3 = """
implementing the bfs algorithm, since it was really challenging
"""
