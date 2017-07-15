#Solves and prints the sudoku position in START
#via depth-first search, fewest-options-first
#the squares are maintained in a min-heap for fewest
#number of available options

import cv2
import math
import copy

START = [0, 0, 0, 0, 0, 0, 6, 8, 0, 
         0, 0, 0, 0, 7, 3, 0, 0, 9,
         3, 0, 9, 0, 0, 0, 0, 4, 5,
         4, 9, 0, 0, 0, 0, 0, 0, 0,
         8, 0, 3, 0, 5, 0, 9, 0, 2,
         0, 0, 0, 0, 0, 0, 0, 3, 6,
         9, 6, 0, 0, 0, 0, 3, 0, 8,
         7, 0, 0, 6, 8, 0, 0, 0, 0,
         0, 2, 8, 0, 0, 0, 0, 0, 0];

class Square:
    def __init__(self):
        self.value = 0                                                  # value of the square, 0 means empty
        self.option = {1: True, 2: True, 3: True, 4: True,              
                       5: True, 6: True, 7: True, 8: True, 9: True}
        self.free = 9                                                   # number of available options
        self.right = Backer(self)                                       # path to next square in row
        self.down = Backer(self)                                        # path to next square in column
        self.next = Backer(self)                                        # path to next square in block
        self.heapIndex = 0                                              # index within the min-heap
        self.boardIndex = 0                                             # index on the board (not needed for solution)
        self.minOption = 1                                              # the min i such that self.option[i] == True
    def off(self, value):                                               # Sets self.option[value] to False
        if(self.option[value]) :
            self.option[value] = False
            self.free -= 1
            while( (self.option.get(self.minOption) == False) & (self.minOption < 10) ) : 
                self.minOption += 1
    def on(self, value):                                                # Sets self.option[value] to True
        if(self.option[value] == False) :
            self.option[value] = True
            self.free += 1
            if(value < self.minOption) : self.minOption = value

class Backer:
    def __init__(self, square):
        self.square = square

class Heap:
    def __init__(self):
        self.size = 81
        self.head = Square()
        self.que = [Square() for i in range (0, 81)]
        self.que[0] = self.head
        self.moves = 0
        self.backtracks = 0

        for i in range (1, 81) :
            self.que[i] = Square()
            self.que[i].heapIndex = i
            self.que[i].boardIndex = i

        for i in range(0, 81) :
            if(i % 9 != 8): self.que[i].right = Backer(self.que[i+1])
            else          : self.que[i].right = Backer(self.que[i-8])

            if(i < 72)    : self.que[i].down = Backer(self.que[i+9])
            else          : self.que[i].down = Backer(self.que[i-72])

            if(i % 3 != 2): self.que[i].next = Backer(self.que[i+1])
            elif(i < 20)  : self.que[i].next = Backer(self.que[i+7])
            elif(i < 29)  : self.que[i].next = Backer(self.que[i-20])
            elif(i < 47)  : self.que[i].next = Backer(self.que[i+7])
            elif(i < 56)  : self.que[i].next = Backer(self.que[i-20])
            elif(i < 74)  : self.que[i].next = Backer(self.que[i+7])
            else          : self.que[i].next = Backer(self.que[i-20])

    def swap(self, index1, index2):
        square = self.que[index1]
        self.que[index1] = self.que[index2]
        self.que[index2] = square

        dummy = self.que[index1].heapIndex
        self.que[index1].heapIndex = self.que[index2].heapIndex
        self.que[index2].heapIndex = dummy

    def heapify(self, index):
        child = index*2
        if(child < self.size):
            if(child+1 < self.size):
                if(self.que[child].free <= self.que[child+1].free):
                    if(self.que[child].free < self.que[index].free):
                        self.swap(index, child)
                        self.heapify(child)
                elif(self.que[child+1].free < self.que[index].free):
                    self.swap(index, child+1)
                    self.heapify(child+1)

    # Assumes 'value' is legal and square is currently set to 0
    def assign(self, index, value):
        self.que[index].value = value
        self.moves += 1
        self.size -= 1

        right              = self.que[index].right.square
        down               = self.que[index].down.square
        next               = self.que[index].next.square
        self.swap(index, self.size)
        self.heapify(0)
        for i in range(0, 9):
            right.off(value)
            j = right.heapIndex
            if(j < self.size):
                while( self.que[j].free < self.que[int(j/2)].free ):
                    self.swap(right.heapIndex, int(right.heapIndex/2))
                    j = int(j/2)
            down.off(value)
            j = down.heapIndex
            if(j < self.size):
                while( self.que[j].free < self.que[int(j/2)].free ):
                    self.swap(down.heapIndex, int(down.heapIndex/2))
                    j = int(j/2)
            next.off(value)
            j = next.heapIndex
            if(j < self.size):
                while( self.que[j].free < self.que[int(j/2)].free ):
                    self.swap(next.heapIndex, int(next.heapIndex/2))
                    j = int(j/2)

            right = right.right.square
            down  = down.down.square
            next  = next.next.square 

    def setBoard(self):
        square = self.head
        for i in range(0, 9):
            for j in range(0, 9):
                k = 9*i+j
                if(START[k] != 0): self.assign( square.heapIndex , START[k] )
                square = square.right.square
            square = square.down.square

    def display(self):
        string = "\n-------------\n"
        square = self.head
        for i in range(0, 9):
            string += "|"
            for j in range(0, 9):
                if(square.value == 0) : string = string + " "
                else                  : string = string + str(square.value)
                if(j % 3 == 2)        : string = string + "|"
                square = square.right.square
            if(i % 3 == 2) : string = string + "\n-------------"
            string = string + "\n"
            square = square.down.square
        string = string + ("Moves: " + str(self.moves))
        string = string + ("\nDead Ends: " + str(self.backtracks))
        print(string)  

    def solve(self):
        if(self.que[0].value > 0) : 
            self.display()
            return True

        if(self.que[0].free <= 0) :
            self.backtracks += 1
            return False

        while(self.que[0].minOption < 10) :
            copyHeap = copy.deepcopy(self)
            copyHeap.assign(0, copyHeap.que[0].minOption)
            if(copyHeap.solve()) : 
                self.backtracks = copyHeap.backtracks
                self.moves = copyHeap.moves
                del copyHeap
                return True
            else : 
                self.backtracks = copyHeap.backtracks
                self.moves = copyHeap.moves
                del copyHeap
                self.que[0].off(self.que[0].minOption)
        self.backtracks += 1
        return False
        

puzzle = Heap()
puzzle.setBoard()
puzzle.display()
puzzle.solve()
