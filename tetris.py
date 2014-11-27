# John Loeber | 26-NOV-2014 | Python 2.7.8 | x86_64 Debian Linux | www.johnloeber.com
from sys import exit
from makecanvas import gridline, blocksize
from ImageColor import getrgb
from random import choice
import pygame
import time

blockimages = {}

class Block(object):
    def __init__(self,color,x,y):
        self.color = color
        self.x = x
        self.y = y
    def getposn(self):
        return = ((blocksize*self.x)+self.x+6,(blocksize*self.y)+self.y+6)
    def getimg(self):
        global blockimages
        return blockimages[self.color]

def makeblockimages():
    """
    Takes the size and colors of the blocks to make images of them.
    """
    global blockimages    
    # Colors of the Tetrominoes
    colors = ["#FFE922","#3CFF2D","#2F3AFF","#990084","#CC1100","#FF7E00","#065C00"]
    for c in colors:
        newblock = pygame.Surface((blocksize,blocksize))
        newblock.fill(getrgb(c))
        blockimages[c] = newblock
    return

def shapedown(blocks,board):
    """
    Moves a shape down one square.
    """
    for block in blocks:
        # make sure the given square is available
        if board[block.x][block.y+1]=='':
            block.y += 1
    

def main():
    makeblockimages()
    pygame.init()
    size = (341,700)

    screen = pygame.display.set_mode(size)

    blocks = [Block("#FFE922",4,0)]    

    background = pygame.image.load("Grid.PNG")
    backgroundcolor = getrgb(gridline)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    shapedown(blocks)
        screen.fill(backgroundcolor)
        # unsure if this use of .blit() is the most efficient I could do
        # on this scale, that probably does not matter
        screen.blit(background,(5,5))
        # blit the known blocks here...
        
        # get rotation...

        # move current block down
        shapedown(blocks,board)
        for block in blocks:
            screen.blit(block.getimg(), block.getposn())
        time.sleep(1)
        pygame.display.flip()

# let's say the user is allowed three 'moves' per downward step

if __name__=='__main__':
    main()
