# John Loeber | 26-NOV-2014 | Python 2.7.8 | x86_64 Debian Linux | www.johnloeber.com
from sys import exit
from makecanvas import gridline, blocksize
from ImageColor import getrgb
from random import choice
import pygame
import time

class Block(object):
    def __init__(self,color,x,y):
        self.color = color
        self.x = x
        self.y = y
    def getposn(self):
        return ((blocksize*self.x)+self.x+6,(blocksize*self.y)+self.y+6)
    def getimg(self):
        global blockimages
        return blockimages[self.color]

blockimages = {}
# Colors of the Tetrominoes
colors = ["#FFE922","#3CFF2D","#2F3AFF","#990084","#CC1100","#FF7E00","#065C00"]
# these define the different shapes. Every shape is on a new line.
shapes = [[Block(colors[0],4,i) for i in range(3)],
          [Block(colors[1],i,0) for i in [3,4,5]].append(Block(colors[1],4,1)),
          [Block(colors[2],i,j) for i in [4,5] for j in [0,1]],
          [Block(colors[3],4,i) for i in range(2)].append(Block(colors[2],5,2)),
          [Block(colors[4],5,i) for i in range(2)].append(Block(colors[2],4,2)),
          [Block(colors[5],4,0),Block(colors[5],4,1),Block(colors[5],3,1),Block(colors[5],5,0)],
          [Block(colors[6],5,0),Block(colors[6],5,1),Block(colors[6],3,0),Block(colors[6],6,1)]]

class Shape(object):
    def __init__(self,color,b1,b2,b3,b4):
        self.color = color
        # the coordinates of b1 are the 'center' of the shape
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4

def newtetromino():
    """
    Returns a random, new tetromino.
    """
    global shapes
    return choice(shapes)

def makeblockimages():
    """
    Takes the size and colors of the blocks to make images of them.
    """
    global blockimages, colors
    for c in colors:
        newblock = pygame.Surface((blocksize,blocksize))
        newblock.fill(getrgb(c))
        blockimages[c] = newblock
    return

def shapemove(blocks,board,x,y):
    """
    Positional translation of blocks by x and y, but checking for possibility
    of such a move first.
    """
    # make sure the given square is available
    available = True
    for block in blocks:
        # try/except to ensure the blocks stay within the bounds of the board
        # assuming the board is of size 10 x 20
        if not (0 <= block.x+x < 10 and 0 <= block.y+y < 20):
            available = False
        elif board[block.x+x][block.y+y]!='':
            available = False
    if available:
        for block in blocks:
            block.x +=x
            block.y +=y
    return   

"""
def shaperotate(blocks,board):
    ...
"""

def main():
    makeblockimages()
    pygame.init()
    size = (341,700)

    screen = pygame.display.set_mode(size)

    blocks = []
    
    blocks.append(randomshape())    
    
    # allows for [x][y] indexing, but is actually a list of columns. A
    # bit unintuitive.
    board = [['']*20]*10
    
    background = pygame.image.load("Grid.PNG")
    backgroundcolor = getrgb(gridline)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    shapemove(blocks,board,0,1)
                elif event.key == pygame.K_LEFT:
                    shapemove(blocks,board,-1,0)
                elif event.key == pygame.K_RIGHT:
                    shapemove(blocks,board,1,0)
                elif event.key == pygame.K_UP:
                    shaperotate(blocks,board)
        screen.fill(backgroundcolor)
        # unsure if this use of .blit() is the most efficient I could do
        # on this scale, that probably does not matter
        screen.blit(background,(5,5))
        # blit the known blocks here...
        
        # get rotation...

        # move current block down
        for block in blocks:
            screen.blit(block.getimg(), block.getposn())
        shapemove(blocks,board,0,1)
        time.sleep(0.5)
        pygame.display.flip()

# let's say the user is allowed three 'moves' per downward step

if __name__=='__main__':
    main()
