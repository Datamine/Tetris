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

class Tetrimino(object):
    def __init__(self,blocks,center):
        self.b1 = blocks[0]
        self.b2 = blocks[1]
        self.b3 = blocks[2]
        self.b4 = blocks[3]
        self.centerx = center[0]
        self.centery = center[1]
        self.rotations = 0
    def blocks(self):
        return [self.b1,self.b2,self.b3,self.b4]

blockimages = {}

# Colors of the Tetriminoes
colors = ["#FFE922","#3CFF2D","#2F3AFF","#990084","#CC1100","#FF7E00","#065C00"]

# define the different tetriminoes. ([Blocks],[Center]): center for rotation
shapes = [# "I"
          Tetrimino([Block(colors[0],4,i) for i in range(4)],[4,1]),
          # "T"
          Tetrimino([Block(colors[1],i,0) for i in [3,4,5]] + [Block(colors[1],4,1)],[4,0]),
          # Square
          Tetrimino([Block(colors[2],i,j) for i in [4,5] for j in [0,1]],[4,0]),
          #  "L"
          Tetrimino([Block(colors[3],4,i) for i in range(3)] + [Block(colors[3],5,2)],[4,1]),
          # Backwards "L"
          Tetrimino([Block(colors[4],5,i) for i in range(3)] + [Block(colors[4],4,2)],[5,1]),
          # "S"
          Tetrimino([Block(colors[5],4,0),Block(colors[5],3,1),Block(colors[5],4,1),Block(colors[5],5,0)],[4,0]),
          # "Z"
          Tetrimino([Block(colors[6],4,0),Block(colors[6],3,0),Block(colors[6],4,1),Block(colors[6],5,1)],[4,0])]

def newtetrimino():
    """
    Returns a random, new tetromino.
    """
    global shapes
    return choice(shapes[5:])

def makeblockimages():
    """
    Takes the size and colors of the blocks to make images of them.
    This is run just once in the start of the game.
    """
    global blockimages, colors
    for c in colors:
        newblock = pygame.Surface((blocksize,blocksize))
        newblock.fill(getrgb(c))
        blockimages[c] = newblock
    return

def shapemove(tetrimino,board,x,y):
    """
    Positional translation of blocks by x and y, but checking for possibility
    of such a move first.
    """
    blocks = tetrimino.blocks()
    # make sure the given square is available
    available = True
    for block in blocks:
        # assuming the board is of size 10 x 20
        if not (0 <= block.x+x < 10 and 0 <= block.y+y < 20):
            available = False
        elif board[block.x+x][block.y+y]!='':
            available = False
    if available:
        for block in blocks:
            block.x +=x
            block.y +=y
        tetrimino.centerx += x
        tetrimino.centery += y
    return   

def handle(tetrimino,board,direction):
    """
    Rotates the "S" and "Z" shapes.
    """
    # detect whether it's oriented horizontally or vertically
    ys = [a.y for a in tetrimino.blocks()]
    rotate = True
    if len(set(ys))==3:
            newb2x = tetrimino.centerx+direction
            newb2y = tetrimino.centery
            
            newb4x = tetrimino.centerx-direction
            newb4y = tetrimino.centery+1
    else:
            newb2x = tetrimino.centerx-direction
            newb2y = tetrimino.centery
            
            newb4x = tetrimino.centerx-direction
            newb4y = tetrimino.centery-1
    try:
        if board[newb2x][newb2y]!='' or board[newb4x][newb4y]!='' or any(item < 0 for item in [newb2x,newb2y,newb4x,newb4y]):
            rotate = False
    except:
        rotate = False
    if rotate:
        tetrimino.b2.x = newb2x
        tetrimino.b2.y = newb2y
    
        tetrimino.b4.x = newb4x
        tetrimino.b4.y = newb4y
    return

def shaperotate(tetrimino,board):
    """
    Rotates a tetrimino.
    """
    c = tetrimino.b1.color
    # Check if tetrimino is a square.
    if c=="#2F3AFF":
        return
    # handle the "S" and "Z" cases. Hardcoding: easier than elegant generalisation.
    elif c == "#FF7E00":
        handle(tetrimino,board,1)
    elif c=="#065C00":
        handle(tetrimino,board,-1)
    else:           
        locs = []
        rotate = True
        for b in tetrimino.blocks():
            xprime = -(b.y - tetrimino.centery) + tetrimino.centerx
            yprime = (b.x-tetrimino.centerx) + tetrimino.centery 
            locs.append((xprime,yprime))
            try:
                if board[xprime][yprime]!='' or xprime<0 or yprime<0:
                    rotate = False
                    break
            except:
                rotate = False
                break
        if rotate:
            #tetrimino.rotations = (tetrimino.rotations +1) %4
            for index, b in enumerate(tetrimino.blocks()):
                b.x = locs[index][0]
                b.y = locs[index][1]
    return

def main():
    makeblockimages()
    pygame.init()
    size = (341,700)

    screen = pygame.display.set_mode(size)

    tetrimino = newtetrimino()
    
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
                    shapemove(tetrimino,board,0,1)
                elif event.key == pygame.K_LEFT:
                    shapemove(tetrimino,board,-1,0)
                elif event.key == pygame.K_RIGHT:
                    shapemove(tetrimino,board,1,0)
                elif event.key == pygame.K_UP:
                    shaperotate(tetrimino,board)
        screen.fill(backgroundcolor)
        # unsure if this use of .blit() is the most efficient I could do
        # on this scale, that probably does not matter
        screen.blit(background,(5,5))
        # blit the known blocks here...
        
        # get rotation...

        # update screen
        for block in tetrimino.blocks():
            screen.blit(block.getimg(), block.getposn())
        # move current block down
        #shapemove(tetrimino,board,0,1)
        time.sleep(0.5)
        pygame.display.flip()

# let's say the user is allowed three 'moves' per downward step

if __name__=='__main__':
    main()
