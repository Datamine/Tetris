# Small script to generate Tetris Canvas
from PIL import Image, ImageDraw
from gameproperties import blocksize, background, gridline

# assuming a 1px divider between every two squares to form the grid,
# and a grid size of 10 by 20 squares
canvasheight = (20 * blocksize) + 21
canvaswidth = (10 * blocksize) + 11

im = Image.new("RGB", (canvaswidth,canvasheight), background)
draw = ImageDraw.Draw(im)

for i in range(0,11):
    draw.line([((blocksize*i)+i,0),((blocksize*i)+i,canvasheight)],fill=gridline)

for j in range(0,21):
    draw.line([(0,(blocksize*j)+j),(canvaswidth,(blocksize*j)+j)],fill=gridline)

im.save("Grid.PNG", "PNG")
