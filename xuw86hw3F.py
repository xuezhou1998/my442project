############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Xuezhou Wen"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
#rom random import choices
import random
import copy
import queue
from queue import PriorityQueue
import math
############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board=[]
    x=0
    for i in range(rows):
        board.append([])
        for j in range(cols):
            x+=1
            if x==cols*rows:

                board[i].append(0)
            else:
                board[i].append(x)
    return TilePuzzle(board)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board=board
        


    def get_board(self):
        return self.board

    def perform_move(self, direction):
        
        board=self.get_board()
        rows=len(board)
        cols=len(board[0])
        coordinates=None
        for i in range(rows):
            for j in range(cols):
                if board[i][j]==0:
                    coordinates=tuple([i,j])
                    break

        replaced_value=None
        to_be_replace=None
        if direction=="up":
            if coordinates[0]==0:
                return False
            else:
                to_be_replace=tuple([coordinates[0]-1,coordinates[1]])
        elif direction=="down":
            if coordinates[0]==rows-1:
                return False
            else:
                to_be_replace=tuple([coordinates[0]+1,coordinates[1]])

        elif direction=="right":
            if coordinates[1]==cols-1:
                return False
            else:
                to_be_replace=tuple([coordinates[0],coordinates[1]+1])

        elif direction=="left":
            if coordinates[1]==0:
                return False
            else:
                to_be_replace=tuple([coordinates[0],coordinates[1]-1])

        for i in range(rows):
            for j in range(cols):
                if tuple([i,j])==to_be_replace:
                    replaced_value=board[i][j]
                    board[i][j]=0
        for i in range(rows):
            for j in range(cols):
                if tuple([i,j])==coordinates:
                    board[i][j]=replaced_value
        self.board=board


        return True



    def scramble(self, num_moves):
        for i in range(num_moves):
            self.perform_move(random.choice(["up","down","left","right"]))

        

    def is_solved(self):
        board=self.get_board()
        rows=len(board)
        cols=len(board[0])
        p=create_tile_puzzle(rows,cols)
        original_board=p.get_board()
        if board==original_board:
            return True
        else:
            return False


    def copy(self):

        #newboard=copy.deepcopy(self.get_board())
        newboard=[]
        board=self.get_board()
        for i in range(len(board)):
            newboard.append([])
            for j in range(len(board[0])):
                newboard[i].append(board[i][j])

        return TilePuzzle(newboard)

    def successors(self):
        choices=["up","down","left","right"]
        

        for i in range(len(choices)):
            p2=self.copy()

            result=p2.perform_move(choices[i])

            if result==True:
                yield tuple([choices[i],p2])  
    def iddfs_helper(self,limit,moves,new):
        
        if moves==None:
            #print("xxxxx")
            moves=[]
        
        if new==None:
            #print("nonenew")
            new=self.copy()
        
        elif new.is_solved()==True:
        #elif new.get_board()==[[1,2,3],[4,5,0]]:
        #else:
            #print("yyy")
            yield moves
        #print(new.board)
        if len(moves)<limit:
            #print(len(moves))
            for addmoves, new_p in new.successors():
                #print(addmoves)
                newmoves=copy.copy(moves)
                newmoves.append(addmoves)
                #print(newmoves)
                yield from self.iddfs_helper(limit,newmoves,new_p)



        


        




    # Required
    def find_solutions_iddfs(self):
        initial_level=0
        while True:
            #print(initial_level)
            g=self.iddfs_helper(initial_level,None,None)
            c=list(g)
            #print(c)
            if c!=[]:
                for i in range(len(c)):

                    yield c[i]
                break
            initial_level+=1





    # Required
    def find_solution_a_star(self):

        #initialization
        a=PriorityQueue()
        path=[(None,-1)]
        board=self.get_board()
        rows=len(board)
        cols=len(board[0])
        goalboard=create_tile_puzzle(rows,cols).get_board()
        if goalboard==board:
            return []
        counter=0
        a.put(tuple([-1,tuple([board,None,0,-1])]))
        #tuple([proirityNumber,tuple([currentBoard,move,cost,IndexOfParent])])
        theSameboard=set()
        final_path=[]
        while a.empty()==False:

            #print(path)
            newNode=a.get()
            #print('selected',newNode[0])
            newInstance=TilePuzzle(newNode[1][0])

            cost=newNode[1][2]
            #print("selected",newNode[1][0])
            if newInstance.is_solved()==True:
                final_path.append(newNode[1][1])
                currentNode=path[newNode[1][3]]
                if currentNode[1]==-1:
                    break
                #print(final_path,currentNode,"final_path")
                while True:
                    final_path.append(currentNode[0])
                    if currentNode[1]==0:
                        break
                    else:
                        
                        currentNode=path[currentNode[1]]


                break
            #if self.Mdistance(goalboard,newNode[1][0])==0:
            #    break
            for move,new_p in newInstance.successors():

                #print(move,new_p.get_board())
                tuplelist=[]
                for i in range(rows):
                        
                    tuplelist.append(tuple(new_p.get_board()[i]))

                tuple_board=tuple(tuplelist)
                if tuple_board not in theSameboard:
                    dis=self.Mdistance(goalboard,new_p.get_board())
                    #print(dis)

                    a.put(tuple([dis+cost,tuple([new_p.get_board(),move,cost+1,path.index(tuple([newNode[1][1],newNode[1][3]]))])]))
                    if path==[]:
                        path.append(tuple([move,None]))
                    else:
                        path.append(tuple([move,path.index(tuple([newNode[1][1],newNode[1][3]]))]))
                    theSameboard.add(tuple_board)
                    
            counter+=1
            #if counter==3:
            #    break
           # path.remove(None)
        #print(final_path,"final_path final_path")
        final_path.reverse()
           #####the problem, you added add steps you have searched, you should only add the steps of the solution into the path!!! 
        return final_path


            

    def Mdistance(self,goalboard,currentboard):
        board=goalboard
        rows=len(board)
        cols=len(board[0])
        mdict={}
        distance=0
        for i in range(rows):
            for j in range(cols):
                mdict[board[i][j]]=tuple([i,j])

        for i in range(rows):
            for j in range(cols):
                newtuple=([i,j])
                oldtuple=mdict[currentboard[i][j]]

                distance+=abs(newtuple[0]-oldtuple[0])+abs(newtuple[1]-oldtuple[1])


        return distance


        

        

        






        

        

############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):
    movelist1=["up","down","right","left"]
    movelist2=["up-left","up-right","down-left","down-right"]
    obstacles=set()
    for i in range(len(scene)):
        for j in range(len(scene[0])):
            if scene[i][j]==True:
                obstacles.add(tuple([i,j]))
    #print("obstacles",obstacles)
    
    #initialization
    a=PriorityQueue()
    
    board=scene
    startCoordinates=start
    path=[(start,-1)]
    rows=len(board)
    cols=len(board[0])
    goalCoordinates=goal
    if goalCoordinates==startCoordinates:
        return []
    counter=0
    a.put(tuple([-1,tuple([start,None,0,-1])]))
    theSameCoordinates=set()
    final_path=[]
    while a.empty()==False:

        #print(path)
        newNode=a.get()
        #print('selected',newNode[0])

        cost=newNode[1][2]
        #print("selected",newNode[1][0])
        if goalCoordinates==newNode[1][0]:
            final_path.append(newNode[1][0])#changed from [1][1] to [1][0]
            currentNode=path[newNode[1][3]]



            if currentNode[1]==-1:
                break
            while True:
                final_path.append(currentNode[0])
                if currentNode[1]==0:
                    break
                else:
                    currentNode=path[currentNode[1]]


            break
        #if self.Mdistance(goalCoordinates,newNode[1][0])==0:
        #    break
        for move,new_p in find_path_successor(newNode[1][0],scene,obstacles):
            #print(move,new_p)

            #print(new_p.get_board())
            #tuplelist=[]
            #for i in range(rows):
                    
             #   tuplelist.append(tuple(new_p.get_board()[i]))

            tuple_coordinates=tuple(new_p)
            if tuple_coordinates not in theSameCoordinates:
                dis=Edistance(goalCoordinates,new_p)
                #print(dis)
                if move in movelist2:
                    currentCost=math.sqrt(2)
                else:
                    currentCost=1
                cost=cost+currentCost
                a.put(tuple([dis+cost,tuple([new_p,move,cost,path.index(tuple([newNode[1][0],newNode[1][3]]))])]))
                if path==[]:
                    path.append(tuple([new_p,None]))
                else:
                    path.append(tuple([new_p,path.index(tuple([newNode[1][0],newNode[1][3]]))]))
                theSameCoordinates.add(tuple_coordinates)
                
        counter+=1
        #if counter==3:
        #    break
       # path.remove(None)
    for x in final_path:
        if x in obstacles:
            return None

    if final_path!=[]:
        final_path.append(startCoordinates)
    else:
        return None
    final_path.reverse()
       #####the problem, you added add steps you have searched, you should only add the steps of the solution into the path!!! 
    return final_path


    
def Edistance(start,end):
    return math.sqrt(abs(start[0]-end[0])**2+abs(start[1]-end[1])**2)
def find_path_successor(coordinates,scene,obstacles):
    movelist=["up","down","right","left","up-left","up-right","down-left","down-right"]
    for i in range(len(movelist)):
        a=find_path_move(movelist[i],coordinates,scene)
        if a!=False and a not in obstacles:
            yield tuple([movelist[i],a])    


def find_path_move(direction,coordinates,scene):
    rows=len(scene)-1
    cols=len(scene[0])-1

    if direction=="up":
        if coordinates[0]!=0:
            coordinates=tuple([coordinates[0]-1,coordinates[1]])
            return coordinates
        else:
            return False

    elif direction=="down":
        if coordinates[0]!=rows:
            coordinates=tuple([coordinates[0]+1,coordinates[1]])
            return coordinates
        else:
            return False

    elif direction=="left":
        if coordinates[1]!=0:
            coordinates=tuple([coordinates[0],coordinates[1]-1])
            return coordinates
        else:
            return False
    elif direction=="right":
        if coordinates[1]!=cols:
            coordinates=tuple([coordinates[0],coordinates[1]+1])
            return coordinates
        else:
            return False

    elif direction=="up-left":
        if coordinates[0]!=0:
            if coordinates[1]!=0:
                coordinates=tuple([coordinates[0]-1,coordinates[1]-1])
                return coordinates
        return False


    elif direction=="up-right":
        if coordinates[0]!=0:
            if coordinates[1]!=cols:
                coordinates=tuple([coordinates[0]-1,coordinates[1]+1])
                return coordinates
        return False


    elif direction=="down-left":
        if coordinates[0]!=rows:
            if coordinates[1]!=0:
                coordinates=tuple([coordinates[0]+1,coordinates[1]-1])
                return coordinates
        return False

    elif direction=="down-right":
        if coordinates[0]!=rows:
            if coordinates[1]!=cols:
                coordinates=tuple([coordinates[0]+1,coordinates[1]+1])
                return coordinates
        return False



    

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def solve_distinct_disks(length, n):
    originalDisk=[]
    for i in range(length):
        if i<n:
            originalDisk.append(i)
        else:
            originalDisk.append(-1)
    goalDisk=copy.deepcopy(originalDisk)
    goalDisk.reverse()
    #initialization
    a=PriorityQueue()
    path=[(None,-1)]
    board=originalDisk
    rows=len(board)
    goalboard=goalDisk
    if goalboard==board:
        return []
    counter=0
    #print(board,"board")
    a.put(tuple([-1,tuple([board,None,0,-1])]))
    #tuple([proirityNumber,tuple([currentBoard,move,cost,IndexOfParent])])
    theSameboard=set()
    final_path=[]
    while a.empty()==False:
        #print("path",path)

        #print(path)
        newNode=a.get()
        #print('selected',newNode[0])
        #newInstance=TilePuzzle(newNode[1][0])

        cost=newNode[1][2]
        #print(newNode[1][0])
        #print("selected",newNode[1][0])
        if is_solved_distinct(newNode[1][0])==True:
            final_path.append(newNode[1][1])
            currentNode=path[newNode[1][3]]
            if currentNode[1]==-1:
                break
            while True:
                #print("1")
                final_path.append(currentNode[0])
                #print(currentNode)
                if currentNode[1]==0:
                    break
                else:
                    currentNode=path[currentNode[1]]


            break
        #if self.Mdistance(goalboard,newNode[1][0])==0:
        #    break
        for move,new_p in disk_successors_distinct(newNode[1][0]):

            #print(new_p.get_board())
            

            tuple_board=tuple(new_p)
            if tuple_board not in theSameboard:
                dis=Ddistance(goalboard,new_p)
                #print(dis)

                a.put(tuple([dis+cost,tuple([new_p,move,cost+1,path.index(tuple([newNode[1][1],newNode[1][3]]))])]))
                if path==[]:
                    path.append(tuple([move,None]))
                else:
                    path.append(tuple([move,path.index(tuple([newNode[1][1],newNode[1][3]]))]))
                theSameboard.add(tuple_board)
                
        counter+=1
        #if counter==3:
        #    break
       # path.remove(None)

    final_path.reverse()
       #####the problem, you added add steps you have searched, you should only add the steps of the solution into the path!!! 
    return final_path





def Ddistance3(goalDisk,newDisk):
    distsum=0
    for i in range(len(goalDisk)):
        if newDisk[i]!=-1:

            a=newDisk[i]
            distsum+=abs(len(newDisk)-newDisk[i]-i)
    return distsum
def Ddistance(goalDisk,newDisk):
    distsum=0
    for i in range(len(goalDisk)):
        if newDisk[i]!=-1:

            a=newDisk[i]
            distsum+=abs(i-goalDisk.index(newDisk[i]))
    return distsum
def Ddistance2(goalDisk,newDisk):
    distsum=0
    for i in range(len(goalDisk)):
        distsum+=abs(goalDisk[i]-newDisk[i])
    return distsum

    
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

############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    initialization=[]
    for i in range(rows):
        initialization.append([])
        for j in range(cols):
            initialization[i].append(False)
    return DominoesGame(initialization)

    

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board=board
        if board!=[]:
            self.rows=len(board)
            self.cols=len(board[0])
        else:
            self.rows=0
            self.cols=0


    def get_board(self):
        return self.board

    def reset(self):
        a=create_dominoes_game(self.rows,self.cols)
        self.board=a.get_board()

    def is_legal_move(self, row, col, vertical):
        board=self.get_board()
        if row<=self.rows-1 and col<=self.cols-1:
            if vertical==True:
                if row<self.rows-1:
                    if board[row][col]==False and board[row+1][col]==False:
                        return True

            else:
                if col<self.cols-1:
                    if board[row][col]==False and board[row][col+1]==False:
                        return True
        return False

    def legal_moves(self, vertical):
        board=self.board
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_legal_move(i,j,vertical)==True:
                    yield tuple([i,j])

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row,col,vertical)==True:
            if vertical==True:
                self.board[row][col]=True
                self.board[row+1][col]=True
            else:
                self.board[row][col]=True
                self.board[row][col+1]=True
        return 



    def game_over(self, vertical):
        if list(self.legal_moves(vertical))==[]:
            return True
        else:
            return False

    def copy(self):
        newboard=[]
        oldboard=self.get_board()
        for i in range(self.rows):
            newboard.append([])
            for j in range(self.cols):
                newboard[i].append(oldboard[i][j])
        return DominoesGame(newboard)

    def successors(self, vertical):
        newInstance=self.copy()

        a=newInstance.legal_moves(vertical)
        for x in a:
            new_p=self.copy()
            new_p.perform_move(x[0],x[1],vertical)
            yield tuple([x,new_p])
        

    def get_random_move(self, vertical):
        a=list(self.legal_moves(vertical))

        return random.choice(a)

    # Required
    def get_best_move(self, vertical, limit):
        if vertical==True:
            a= self.VerticalValue(self.get_board(),-(limit*self.rows*self.cols),limit*self.rows*self.cols,0,limit,0)
            return tuple([a[0],a[1],a[2]+1])
        else:
            a= self.HorizontalValue(self.get_board(),-(limit*self.rows*self.cols),limit*self.rows*self.cols,0,limit,0)
            return tuple([a[0],-a[1],a[2]+1])






    def VerticalValue(self,state,a,b,depth,limit,leaves):
        #print("pasV")
        if depth>=limit:
            #print("None VerticalValue")
            return tuple([None,self.Utility(state,True),leaves])
        newInstance=DominoesGame(state)
        v=-(limit*self.rows*self.cols)
        depth+=1
        leaves2=leaves
        selected=None
        counter=0
        for x,y in newInstance.successors(True):
            counter+=1
            #print("x of VerticalValue",x,depth,a,b)
            leaves2+=1
            vold=v
            rDeeper=self.HorizontalValue(y.get_board(),a,b,depth,limit,leaves2)
            #print(rDeeper)
            v=max(v,rDeeper[1])
            leaves2=rDeeper[2]
            if v>vold:
                selected=x
            if v>=b:
                #print("pasV2")
                return tuple([selected,v,leaves2-1])
            a=max(a,v)
        #print("pasV3")
        if counter==0:
            return tuple([None,self.Utility(state,True),leaves])
        return tuple([selected,v,leaves2-1])



    def HorizontalValue(self,state,a,b,depth,limit,leaves):
        #print("pasH")
        if depth>=limit:
            #print("None HorizontalValue")
            return tuple([None,self.Utility(state,False),leaves])
        newInstance=DominoesGame(state)
        v=limit*self.rows*self.cols
        depth+=1
        leaves2=leaves
        selected=None
        counter=0
        for x,y in newInstance.successors(False):
            counter+=1
            #print("x of HorizontalValueH", x,depth,a,b)
            leaves2+=1
            vold=v
            rDeeper=self.VerticalValue(y.get_board(),a,b,depth,limit,leaves2)
            #print(rDeeper)
            v=min(v,rDeeper[1])
            leaves2=rDeeper[2]
            if v<vold:
                selected=x
            if v<=a:
                #print("pasH2")
                return tuple([selected,v,leaves2-1])
            b=min(b,v)
        #print("pasH3")
        if counter==0:
            return tuple([None,self.Utility(state,False),leaves])
        return tuple([selected,v,leaves2-1])
        
    def Utility(self,state,vertical):
        a=DominoesGame(state)
        #if vertical==True:
        #    
        #else:
        #    return len(list(a.legal_moves(False)))-len(list(a.legal_moves(True)))
        return len(list(a.legal_moves(True)))-len(list(a.legal_moves(False)))


############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
16hours
"""

feedback_question_2 = """
the aspect of implementing the algorithm is the most challenging.
i encountered a stumbling block when doing the domenoesgame problem.
"""

feedback_question_3 = """
i like the algorithm part of this assignment. the change i hope for is 
to give some scores to infrasctrature in this assignment. 
"""
