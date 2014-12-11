# John Loeber | 26-NOV-2014 | Python 2.7.8 | x86_64 Debian Linux | www.johnloeber.com

from sys import exit
from makecanvas import gridline, blocksize
from ImageColor import getrgb
from random import choice
from copy import deepcopy
from os.path import expanduser
import time
import pygame

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
    def blocks(self):
        return [self.b1,self.b2,self.b3,self.b4]
    def getcoords(self):
        return [(b.x,b.y) for b in self.blocks()]

blockimages = {}

# Colors of the Tetriminoes, white for the flashing effect
colors = ["#FFE922","#3CFF2D","#2F3AFF","#990084","#CC1100","#FF7E00",
          "#065C00","#FFFFFF"]

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
    global shapes
    return deepcopy(choice(shapes))

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
        if board[newb2x][newb2y]!='' or board[newb4x][newb4y]!='' or \
           any(item < 0 for item in [newb2x,newb2y,newb4x,newb4y]):
            rotate = False
    except:
        rotate = False
    if rotate:
        tetrimino.b2.x = newb2x
        tetrimino.b2.y = newb2y
    
        tetrimino.b4.x = newb4x
        tetrimino.b4.y = newb4y
    return

def drop(tetrimino,board):
    """
    Drops a piece.
    """
    prev = deepcopy(tetrimino)
    shapemove(tetrimino,board,0,1)
    while prev.getcoords()!=tetrimino.getcoords():
        shapemove(prev,board,0,1)
        shapemove(tetrimino,board,0,1)
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

def blitboard(board,screen):
    for y in board:
        for x in y:
            if x!='':
                screen.blit(x.getimg(),x.getposn())
    return

def maketext(screen,blacklines,whitelines,posns):
    for i in range(len(blacklines)):
        offone = (posns[i][0]+2,posns[i][1]+2)
        offtwo = (posns[i][0]-2,posns[i][1]-2)
        offthree = (posns[i][0]+2,posns[i][1]-2)
        offfour = (posns[i][0]-2,posns[i][1]+2)
        screen.blit(blacklines[i],offone)
        screen.blit(blacklines[i],offtwo)
        screen.blit(blacklines[i],offthree)
        screen.blit(blacklines[i],offfour)
        screen.blit(whitelines[i],posns[i])
    pygame.display.flip()
    return

def gameover(screen):
    global typeface
    lines = ['Game Over','Hit ENTER to play again','ESC to quit', 'M for main menu']
    blacklines = [typeface.render(i,1,getrgb("#000000")) for i in lines]
    whitelines = [typeface.render(i,1,getrgb("#FFFFFF")) for i in lines]
    # calculated the positions by hand and hardcoded them
    posns = [(116,247),(46,306),(112,360),(83,414)]
    maketext(screen,blacklines,whitelines,posns)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)
                elif event.key == pygame.K_m:
                    return 9
                elif event.key == pygame.K_n:
                    return 1
                elif event.key == pygame.K_RETURN:
                    return 1

def pause(screen):
    global typeface
    lines = ['Paused',"Hit p to resume"]
    blacklines = [typeface.render(i,1,getrgb("#000000")) for i in lines]
    whitelines = [typeface.render(i,1,getrgb("#FFFFFF")) for i in lines]
    print blacklines[1].get_rect().width
    posns = [(133,309),(89,353)]
    maketext(screen,blacklines,whitelines,posns)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return

# retrieve max score from the store-file
def getmaxlines():
    try:
        with open(expanduser("~/.jtetris.txt"),"r") as f:
            return f.readlines()[1].rstrip('\n')
    except:
        return "0"

# write max score to the store-file
def writemaxlines(n):
    # Can do this w/o rewriting msg every time. Not important on this scale.
    message = ("This file was generated by tetris.py. It keeps track of your "
               "max score in the Tetris game. For documentation, see"
               " http://www.johnloeber.com/docs/tetris.html.\n")
    try:
        with open(expanduser("~/.jtetris.txt"),"w") as f:
            f.write(message+str(n))
    except:
        return

def check(board,screen):
    b2 = deepcopy(board)
    effect = False
    rows = []
    for i in range(20):
            row = [b2[x][i] for x in range(10)]
            if all(i!='' for i in row):
                rows.append(i)
                for t in row:
                    t.color="#FFFFFF"
                effect=True
    lrows = len(rows)
    if effect:
        blitboard(b2,screen)
        pygame.display.flip()
        time.sleep(0.02)
        blitboard(board,screen)
        pygame.display.flip()
        time.sleep(0.02)
        blitboard(b2,screen)
        pygame.display.flip()
        while rows:
            current = max(rows)
            for i in range(10):
                for j in range(current):
                    if board[i][j]!='':
                        board[i][j].y += 1
                del board[i][current]
                board[i] = [''] + board[i]
            rows.remove(current)
            rows = map(lambda y: y+1,rows)
    return lrows

def game(screen,startinglevel):
    cleared = 0
    tetrimino = newtetrimino()
    bestscore = int(getmaxlines())

    # allows for [x][y] indexing, but is actually a list of columns. A
    # bit unintuitive.
    board = [['']*20 for n in range(10)]
    
    background = pygame.image.load("Grid.PNG")
    backgroundcolor = getrgb(gridline)
    timestep = time.time()
    
    bottom = pygame.font.Font('BebasNeue.ttf',20)
    white = getrgb("#FFFFFF")
    
    while True:
        level = cleared/10 + startinglevel
        timeinterval = 0.75*(0.95**level)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    shapemove(tetrimino,board,0,1)
                elif event.key == pygame.K_LEFT:
                    shapemove(tetrimino,board,-1,0)
                elif event.key == pygame.K_RIGHT:
                    shapemove(tetrimino,board,1,0)
                elif event.key == pygame.K_UP:
                    shaperotate(tetrimino,board)
                elif event.key == pygame.K_ESCAPE:
                    exit(0)
                elif event.key == pygame.K_n:
                    return 1
                elif event.key == pygame.K_m:
                    return 9
                elif event.key == pygame.K_p:
                    pause(screen)
                elif event.key == pygame.K_SPACE:
                    drop(tetrimino,board)
   
        x = 0
        x = check(board,screen)
        cleared += x
        newpiece = False
        if cleared > bestscore:
            writemaxlines(cleared)
            bestscore = cleared
        coords = tetrimino.getcoords()
        for c in coords:
            if c[1]==19:
                newpiece=True
                break
            try:
                if board[c[0]][c[1]+1]!='':
                    newpiece=True
                    break
            except:
                print "Unexpected Error"
        if newpiece:
            for t in tetrimino.blocks():
                board[t.x][t.y] = t
            tetrimino = newtetrimino()
            coords = tetrimino.getcoords()
            for (x,y) in coords:
                if board[x][y]!='':
                    returnstatus = gameover(screen)
                    return returnstatus
        else:
            newt = time.time()
            if timestep+timeinterval < newt:
                # move current block down
                shapemove(tetrimino,board,0,1)
                timestep = newt        

        #print "Cleared: ", cleared, "Level: ", level, "Interval: ", timeinterval
        # unsure if this use of .blit() is the most efficient I could do
        # on this scale, that probably does not matter

        screen.fill(backgroundcolor)
        screen.blit(background,(5,5))

        leveltext = bottom.render("Level: " + str(level+1),1,white)
        clearedtext = bottom.render("Lines: " + str(cleared),1,white)
        besttext = bottom.render("Best: " + str(bestscore),1,white)
    
        screen.blit(leveltext,(10,675))
        screen.blit(clearedtext,((341-clearedtext.get_rect().width)/2,675))
        screen.blit(besttext,(331-(besttext.get_rect().width),675))

        # blit the known blocks here...
        blitboard(board,screen)
        
        # update screen
        for block in tetrimino.blocks():
            screen.blit(block.getimg(), block.getposn())
        pygame.display.flip()

def getlevel(screen,color,typeface):
    highlight = getrgb("#3CFF2D")
    screen.fill(getrgb("#000000"))
    levels = range(1,101)
    lines = [typeface.render(str(i),1,color) for i in levels]
    ranges = [range(a,b) for (a,b) in [(0,20),(20,40),(40,60),(60,80),(80,100)]]
    locs = []
    rectangles = {}
    for j in zip(ranges,[57,114,171,228,285]):
        for k in j[0]:
            w = lines[k].get_rect().width/2
            h = 32
            x = j[1]-w
            y = (34*(k%20))+10
            screen.blit(lines[k],(x,y))
            locs.append((x,y))
            rectangles[(x,y,x+(2*w),y+h)] = k
    pygame.display.flip()
    active = []
    while True:
        # not sure exactly why the next two lines work
        for event in pygame.event.get():
            x,y = pygame.mouse.get_pos()
            # could make this a lot faster, but whatever
            for (x1,y1,x2,y2) in rectangles:
                if (x1 <= x <= x2) and (y1 <= y <= y2):
                    current = rectangles[(x1,y1,x2,y2)]
                    if current not in active: 
                        active.append(current)
                        screen.blit(typeface.render(str(levels[current]),1,highlight),(x1,y1))
                        pygame.display.flip()
            if len(active) > 1:
                delete = active[0]
                pygame.draw.rect(screen,getrgb("#000000"),(locs[delete][0],locs[delete][1],35,32))
                screen.blit(lines[delete],locs[delete])
                pygame.display.flip()
                del active[0]
            if any(x==1 for x in pygame.mouse.get_pressed()):
                print active[0]
                return active[0]

def start(screen):
    title = pygame.font.Font('BebasNeue.ttf',72)
    instruct = pygame.font.Font('BebasNeue.ttf',26)
    color = getrgb("#FFFFFF")
    screen.fill(getrgb("#000000"))
    lines = ['Hit ENTER to play',"ESC to quit","P to pause",
             "N for new game", "L to change starting level",
             "M for main menu", "Arrow keys and space to move"]

    tetris = title.render("TETRIS",1,color)
    whitelines = [instruct.render(i,1,color) for i in lines]
    posns = [(93,246),(121,293),(124,340),(102,387),(50,481),(98,434),(34,528)]
    screen.blit(tetris,(95,139))
    for i in range(len(posns)):
        screen.blit(whitelines[i],posns[i])
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 0
                elif event.key == pygame.K_l:
                    return getlevel(screen,color,instruct)
                elif event.key == pygame.K_ESCAPE:
                    exit(0)

def handler(screen,startinglevel):
    while True:
        x = game(screen,startinglevel)
        if x==9:
            return

def metahandler(screen):
    while True:
        startinglevel = start(screen)
        handler(screen,startinglevel)

def main():
    makeblockimages()
    pygame.init()
    size = (341,700)
    screen = pygame.display.set_mode(size)
    global typeface
    typeface = pygame.font.Font('BebasNeue.ttf',32)

    metahandler(screen)

if __name__=='__main__':
    main()
