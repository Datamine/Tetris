# John Loeber | Nov 26 | Python 2.7.8 | x86_64 Debian Linux | www.johnloeber.com
from sys import exit
from makecanvas import gridline, blocksize
from PIL import ImageColor
from random import choice
import pygame
import time

class Block(object):
    def __init__(self,color,x,y):
        self.color = color
        self.x = x
        self.y = y
    def down(self):
        self.y -= 1
    def getposn(self):
        return ((blocksize*self.x)+self.x,(blocksize*self.y)+self.y)
    def getimg(self):
        return 
"""
class Shape(object):
    def __init__(self,b1,b2,b3,b4):
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4
    def rotate(self):
        
        
        
    # Colors of the Tetrominoes
    colors = ["#FFE922","#3CFF2D","#2F3AFF","#990084","#CC1100","#FF7E00","#065C00"]
   
"""  

def main():
    pygame.init()
    size = (341,700)

    screen = pygame.display.set_mode(size)

    blocks = [Block("#FFE922",4,0)]    

    background = pygame.image.load("Grid.PNG")
    backgroundcolor = ImageColor.getrgb(gridline)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        screen.fill(backgroundcolor)
        # unsure if this use of .blit() is the most efficient I could do
        # on this scale, that probably does not matter
        screen.blit(background,(5,5))
        # blit the known blocks here...
        
        # get rotation...

        # move current block down
        for block in blocks:
            block.down()
        for block in blocks:
            screen.blit(block.getimg(), block.getposn())
        time.sleep(0.1)
        pygame.display.flip()

# let's say the user is allowed three 'moves' per downward step

if __name__=='__main__':
    main()
