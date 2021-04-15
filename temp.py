# -*- coding: utf-8 -*-
"""
Spyder Editor

xmin = 480
xmax = 1440
ymin = 300
ymax = 800

"black" = [0,0,0]
"dark_grey" = [102,102,10]
"dark_blue" = [0,80,205]
"white" = [255,255,255]
"light_grey" = [170,170,170]
"light_blue" = [38,201,25]
"dark_green" = [1,116,32]
"dark_marron" = [105,21,6]
"light_marron" = [150, 65, 18]
"light_green" = [17,176,60]
"red" = [255,0,19]
"orange" = [255,120,4]
"dirt_yellow" = [176,112,2]
"purple" = [153,0,76]
"beige" = [203,90,87]
"yellow" = [255,193,3]
"light_beige" = [254,175,16]
"""
xmin = 480
xmax = 1440
ymin = 300
ymax = 800
COLORS = [
(0,0,0),

(0,80,205),
(255,255,255),
(170,170,170),
(38,201,255),
(1,116,32),
(105,21,6),
(150, 65, 18),
(17,176,60),
(255,0,19),
(255,120,41),
(176,112,28),
(153,0,78),
(203,90,87),
(255,193,38),
(255,0,143),
(254,175,168),
    ]
COLORS = set(COLORS)

from pynput.mouse import Button, Controller
import multiprocessing
# import the necessary packages
import numpy as np

import time
from PIL import Image, ImageEnhance
import numpy as np
from itertools import chain
import pyautogui
from math import sqrt
from functools import lru_cache


mouse = Controller()
s = pyautogui.screenshot()
s = s.crop((0,0,480,1000))
size = s.size
s = s.load()

colorsCoord = dict()

def clickMouse(x ,y):
    x = x+xmin
    y = y+ymin
    mouse.position = (x, y)
    mouse.click(Button.left,1)

def clickColor(x,y):
    mouse.position = (x, y)
    mouse.click(Button.left,1)

def loadImage():
    image = Image.open("tortu.png").convert("RGB")
    return image

def computeImage(image):
    size = ( ymax-ymin,xmax-xmin)
    size = (500, 500)
    image = image.resize(size)
    image = image.rotate(90)
    enhancer = ImageEnhance.Contrast(image)

    pixels = np.array(image)
    return pixels

def draw(pixels):
    i, j, osef = pixels.shape
    selectedColor = (1,1,1)
    for x in range(0,i,2):
        for y in range(0,j,2):
            actualPixel = tuple(pixels[x,y])
            if(actualPixel != (0,0,0)):
                if(actualPixel != selectedColor):
                    selectColor(actualPixel)
                    selectedColor = actualPixel
                clickMouse(x,y)
        
def selectColor(color):
    x,y = colorsCoord[color]
    mouse.position = (x,y)
    mouse.click(Button.left, 1)
    
    
def setColorsCoord():
    for x in range(size[0]):
        for y in range(size[1]):
            if (s[x,y] in COLORS):
                colorsCoord[s[x,y]] = x,y

@lru_cache()
def giveClosestColor(rgb):
    r, g, b = rgb[:3]
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))

    return min(color_diffs)[1]

def updateColors(pixels):
    i, j, osef = pixels.shape
    for x in range(i):
        for y in range(j):
            pixels[x,y] = giveClosestColor(tuple(pixels[x,y]))
    return pixels

if __name__ == '__main__':
    temps = time.time()
    setColorsCoord()
    image = loadImage()
    pixels = computeImage(image)
    pixels = updateColors(pixels)
    #Image.fromarray(pixels).show()
    draw(pixels)
    print(time.time()-temps)
    
    '''
    OLD WAY
    
def color_difference (color1, color2):
    return sum([abs(component1-component2) for component1, component2 in zip(color1, color2)])


def giveClosestColor(my_color):
    differences = [[color_difference(my_color, target_value), target_name] for target_name, target_value in TARGET_COLORS.items()]
    differences.sort() 
    my_color_name = differences[0][1]
    rgb = TARGET_COLORS[my_color_name]
    return rgb

COLORS = {
   "black" : (0,0,0),
    "dark_grey" : (102,102,102),
    "dark_blue" : (0,80,205),
    "white" : (255,255,255),
    "light_grey" : (170,170,170),
    "light_blue" : (38,201,255),
    "dark_green" : (1,116,32),
    "dark_marron" : (105,21,6),
    "light_marron" : (150, 65, 18),
    "light_green" : (17,176,60),
    "red" : (255,0,19),
    "orange" : (255,120,41),
    "dirt_yellow" : (176,112,28),
    "purple" : (153,0,78),
    "beige" : (203,90,87),
    "yellow" : (205,193,38),
    "pink" : (255,0,143),
    "light_beige" : (254,175,168),
    }
'''