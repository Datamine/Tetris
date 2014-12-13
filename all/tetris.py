# John Loeber | 26-NOV-2014 | Python 2.7.8 | x86_64 Debian Linux | www.johnloeber.com

from gameproperties import gridline
from tscore import getmaxlines, writemaxlines
from blocks import *

from sys import exit
from ImageColor import getrgb
import time
import pygame

################################################################################
    
##  Configuring Block Images

blockimages = {}

def getimg(Block):
    """
    Returns the pygame image representing a block.
    """
    return blockimages[Block.color]

def makeblockimages():
    """
    Takes the size and colors of the blocks to make images of them.
    This is run just once in the start of the game.
    """
    for c in colors:
        newblock = pygame.Surface((blocksize,blocksize))
        newblock.fill(getrgb(c))
        blockimages[c] = newblock
    return

################################################################################

##  Moving and Rotating Tetriminoes

def shapemove(tetrimino,board,x,y):
    """
    Positional translation of blocks by x and y, but checking for possibility
    of such a move first.
    """
    blocks = tetrimino.blocks()
    # make sure that for each block, the next square is available.
    available = True
    for block in blocks:
        # assuming the board is of size 10 x 20
        if not (0 <= block.x+x < 10 and 0 <= block.y+y < 20):
            available = False
        elif board[block.x+x][block.y+y]!='':
            available = False
    # if each block can move, then all blocks are moved.
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
    ys = len(set([a.y for a in tetrimino.blocks()]))
    rotate = True
    if ys==3:
            # note that block1 and block3 stay in constant position,
            # so we only need to check the potential location of blocks 2 & 4
            newb2x = tetrimino.centerx+direction
            newb2y = tetrimino.centery
            
            newb4x = tetrimino.centerx-direction
            newb4y = tetrimino.centery+1
    else:
            newb2x = tetrimino.centerx-direction
            newb2y = tetrimino.centery
            
            newb4x = tetrimino.centerx-direction
            newb4y = tetrimino.centery-1
    # checks all of the potential block-locations for availability.
    try:
        if board[newb2x][newb2y]!='' or board[newb4x][newb4y]!='' or \
           any(item < 0 for item in [newb2x,newb2y,newb4x,newb4y]):
            rotate = False
    except:
        rotate = False
    # rotates the shape if positions for blocks 2 and 4 are available.
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
    # move the tetrimino downwards until this no longer does anything.
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
        # rotation of points on a cartesian plane           
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

################################################################################

## Pause, Gameover, and GetLevel Screens

def maketext(screen,blacklines,whitelines,posns):
    """
    Makes white text with a black stroke for the GameOver and Pause screens.
    """
    for i in range(len(blacklines)):
        # a stroke is achieved by rendering black text and offsetting it
        # by 2 px in each direction
        offone = (posns[i][0]+2,posns[i][1]+2)
        offtwo = (posns[i][0]-2,posns[i][1]-2)
        offthree = (posns[i][0]+2,posns[i][1]-2)
        offfour = (posns[i][0]-2,posns[i][1]+2)
        for j in [offone,offtwo,offthree,offfour]:
            screen.blit(blacklines[i],j)
        screen.blit(whitelines[i],posns[i])
    pygame.display.flip()
    return

def makelines():
    """
    Makes lines for the gameover and pause screens. This runs just once in the
    start, to prevent unneccessary repeated executions.
    """
    global GOblacklines, GOwhitelines, Pblacklines, Pwhitelines
    GOlines = ['Game Over','Hit ENTER to play again','ESC to quit', 'M for main menu']
    Plines = ['Paused',"Hit p to resume"]
    typeface = pygame.font.Font('BebasNeue.ttf',32)
    GOblacklines = [typeface.render(i,1,getrgb("#000000")) for i in GOlines]
    GOwhitelines = [typeface.render(i,1,getrgb("#FFFFFF")) for i in GOlines]
    Pblacklines = [typeface.render(i,1,getrgb("#000000")) for i in Plines]
    Pwhitelines = [typeface.render(i,1,getrgb("#FFFFFF")) for i in Plines]
    return 

def gameover(screen):
    """
    Blits the gameover menu.
    """
    # calculated the positions by hand and hardcoded them
    posns = [(116,247),(46,306),(112,360),(83,414)]
    maketext(screen,GOblacklines,GOwhitelines,posns)
    while True:
        # keystroke handling
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
    """
    Blits the pause dialogue.
    """
    posns = [(133,309),(89,353)]
    maketext(screen,Pblacklines,Pwhitelines,posns)
    while True:
        # keystroke handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return
                elif event.key == pygame.K_ESCAPE:
                    exit(0)

def getlevel(screen,color,typeface):
    """
    Blits the getlevel menu, and returns the level the user selects.
    """
    highlight = getrgb("#3CFF2D")
    screen.fill(getrgb("#000000"))
    levels = range(1,101)
    lines = [typeface.render(str(i),1,color) for i in levels]
    # each range is for a column. Five columns of 20 levels each.
    ranges = [range(a,b) for (a,b) in [(0,20),(20,40),(40,60),(60,80),(80,100)]]
    locs = []
    rectangles = {}
    # the list [57..285] represents the y-locations of each column.
    for j in zip(ranges,[57,114,171,228,285]):
        for k in j[0]:
            # center the text on the column
            w = lines[k].get_rect().width/2
            h = 32
            x = j[1]-w
            # %20 to divide the 100 levels into 5 columns. 34 is vertical px
            # distance between entries.
            y = (34*(k%20))+10
            screen.blit(lines[k],(x,y))
            # locs: map every level to (x,y) coord denoting start of rectangle
            locs.append((x,y))
            # rectangles: map every rectangle to its level.
            rectangles[(x,y,x+(2*w),y+h)] = k
    pygame.display.flip()
    # active: the level the user has moved their cursor over
    active = []
    while True:
        for event in pygame.event.get():
            x,y = pygame.mouse.get_pos()
            # could make this faster, but this is small-scale.
            for (x1,y1,x2,y2) in rectangles:
                # finds the rectangle the cursor is in
                if (x1 <= x <= x2) and (y1 <= y <= y2):
                    current = rectangles[(x1,y1,x2,y2)]
                    if current not in active: 
                        active.append(current)
                        # makes the text in the current rectangle green
                        screen.blit(typeface.render(str(levels[current]),1,highlight),(x1,y1))
                        pygame.display.flip()
            if len(active) > 1:
                # if the user has moved the cursor to another rectangle: make
                # the text in the previous rectangle white again.
                delete = active[0]
                pygame.draw.rect(screen,getrgb("#000000"),
                                 (locs[delete][0],locs[delete][1],35,32))
                screen.blit(lines[delete],locs[delete])
                pygame.display.flip()
                del active[0]
            if any(x==1 for x in pygame.mouse.get_pressed()):
                # if user clicks in rectangle: return the corresponding level
                return active[0]
            if event.type == pygame.QUIT: 
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)
         
################################################################################

## Other game internals

def blitboard(board,screen):
    """
    Blits all blocks in the board to the screen.
    """
    for y in board:
        for x in y:
            if x!='':
                screen.blit(getimg(x),x.getposn())
    return

def check(board,screen):
    """
    Checks for completed lines, and clears them.
    """
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
        # flashing effect when line clears
        blitboard(b2,screen)
        pygame.display.flip()
        time.sleep(0.02)
        blitboard(board,screen)
        pygame.display.flip()
        time.sleep(0.02)
        blitboard(b2,screen)
        pygame.display.flip()
        while rows:
            # for each of the cleared rows: remove it from the board, 
            # and add a new empty row at the top. also, advance the y-coord
            # of any blocks above.
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
    """
    The tetris-game itself. Handles user input to move, etc.
    """
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
        # amount of time in-between automatic block movements down
        timeinterval = 0.75*(0.95**level)
        for event in pygame.event.get():
            # keystroke handling
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

        # check for full lines and clears them 
        x = 0
        x = check(board,screen)
        cleared += x
        newpiece = False
        # update the score
        if cleared > bestscore:
            writemaxlines(cleared)
            bestscore = cleared
        coords = tetrimino.getcoords()
        # check if a new piece should be spawned
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
            # if a new piece is spawned, then we write the current piece
            # to the board.
            for t in tetrimino.blocks():
                board[t.x][t.y] = t
            tetrimino = newtetrimino()
            coords = tetrimino.getcoords()
            # check if the new piece has space to be spawned. else: gameover
            for (x,y) in coords:
                if board[x][y]!='':
                    returnstatus = gameover(screen)
                    return returnstatus
        else:
            # check if the piece should be moved down
            newt = time.time()
            if timestep+timeinterval < newt:
                # move current block down
                shapemove(tetrimino,board,0,1)
                timestep = newt        

        # unsure if this use of .blit() is the most efficient I could do
        # on this scale, that probably does not matter

        screen.fill(backgroundcolor)
        screen.blit(background,(5,5))

        # update the information at the bottom of the screen

        leveltext = bottom.render("Level: " + str(level+1),1,white)
        clearedtext = bottom.render("Lines: " + str(cleared),1,white)
        besttext = bottom.render("Best: " + str(bestscore),1,white)
    
        screen.blit(leveltext,(10,675))
        screen.blit(clearedtext,((341-clearedtext.get_rect().width)/2,675))
        screen.blit(besttext,(331-(besttext.get_rect().width),675))

        # blit the known blocks
        blitboard(board,screen)
        
        # update screen
        for block in tetrimino.blocks():
            screen.blit(getimg(block), block.getposn())
        pygame.display.flip()

def start(screen):
    """
    Blits the start-menu.
    """
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
        # keystroke handling
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

def main():
    makeblockimages()
    pygame.init()
    size = (341,700)
    screen = pygame.display.set_mode(size)
    
    makelines()    

    while True:
        startinglevel = start(screen)
        while True:
            x = game(screen,startinglevel)
            if x==9:
                break


if __name__=='__main__':
    main()
