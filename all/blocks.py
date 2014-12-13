from gameproperties import blocksize,colors
from copy import deepcopy
from random import choice

class Block(object):
    """
    To represent one of the four constituents of each Tetrimino.
    """
    def __init__(self,color,x,y):
        self.color = color
        self.x = x
        self.y = y
    def getposn(self):
        return ((blocksize*self.x)+self.x+6,(blocksize*self.y)+self.y+6)

class Tetrimino(object):
    """
    A tetrimino is one of the seven possible contiguous collections of blocks.
    """
    def __init__(self,blocks,center):
        self.b1 = blocks[0]
        self.b2 = blocks[1]
        self.b3 = blocks[2]
        self.b4 = blocks[3]
        self.centerx = center[0]
        self.centery = center[1]
    def blocks(self):
        return [self.b1,self.b2,self.b3,self.b4]
    def getcoords(self):
        return [(b.x,b.y) for b in self.blocks()]

# define the different tetriminoes. ([Blocks],[Center]): center for rotation
shapes = [# "I"
          Tetrimino([Block(colors[0],4,i) for i in range(4)],[4,1]),
          # "T"
          Tetrimino([Block(colors[1],i,0) for i in [3,4,5]] + \
                    [Block(colors[1],4,1)],[4,0]),
          # Square
          Tetrimino([Block(colors[2],i,j) for i in [4,5] for j in [0,1]],[4,0]),
          #  "L"
          Tetrimino([Block(colors[3],4,i) for i in range(3)] + \
                    [Block(colors[3],5,2)],[4,1]),
          # Backwards "L"
          Tetrimino([Block(colors[4],5,i) for i in range(3)] + \
                    [Block(colors[4],4,2)],[5,1]),
          # "S"
          Tetrimino([Block(colors[5],4,0),Block(colors[5],3,1),\
                     Block(colors[5],4,1),Block(colors[5],5,0)],[4,0]),
          # "Z"
          Tetrimino([Block(colors[6],4,0),Block(colors[6],3,0),\
                     Block(colors[6],4,1),Block(colors[6],5,1)],[4,0])]

def newtetrimino():
    """
    Returns a random, new tetrimino.
    """
    return deepcopy(choice(shapes))
