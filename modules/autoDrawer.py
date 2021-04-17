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
xmin = 550
xmax = 1440
ymin = 350
ymax = 800
COLORS = {
(0,80,205),
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
    }



import multiprocessing
# import the necessary packages
import numpy as np

import time
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
from itertools import chain
import pyautogui
from math import sqrt
from functools import lru_cache
import imghdr
import requests


pyautogui.PAUSE = 0.01

class AutoDrawer(object):
    def __init__(self):
        self.drawAreaConfigured = False
        self.colorAreaConfigured = False
        self.imageConfigured = False
        self.colorsCoord = dict()
        self.loaded = 0
        self.compression = 10
        
    def setupDrawArea(self, start, end):
        self.drawStart = start
        self.drawEnd = end
        self.drawAreaConfigured = True
        
    def setupColorArea(self, start, end):
        self.colorAreaStart = start
        self.colorAreaEnd = end
        self.getColors()
        self.colorAreaConfigured = True
        
    def setupImage(self, image):
        self.image = image
        self.imageConfigured = True
    
    def check(self):
        if(self.loaded == 1):
            return ("Prêt", 3)
        if(self.loaded == 2):
            return ("En cours", 2)
        if(self.drawAreaConfigured == False):
            return ("Zone de dessin non configurée", 100)
        if(self.colorAreaConfigured == False):
            return ("Zone des couleurs non configurée", 101)
        if(self.imageConfigured == False):
            return ("Pas d'image chargée", 102)
        return ("Prêt", 1)
        
    def getColors(self):
        colorScreenshot = pyautogui.screenshot().load()
        for x in range(self.colorAreaStart[0], self.colorAreaEnd[0], 1):
            for y in range(self.colorAreaStart[1], self.colorAreaEnd[1],1):
                if (colorScreenshot[x,y] in COLORS):
                    self.colorsCoord[colorScreenshot[x,y]] = x,y
                    
    def clickMouse(self, x, y):
        x = x + self.drawStart[0]
        y = y + self.drawStart[1]
        pyautogui.click(x,y, 1)
        
    def dragMouse(self, x, y):
        x = x + self.drawStart[0]
        y = y + self.drawStart[1]
        pyautogui.dragTo(x,y, button='left')

    def clickColor(self, x ,y ):
        pyautogui.click(x, y)
        
    def loadImage(self, url):
        try:
            image = requests.get(url, stream=True).raw
            image = Image.open(image)
        except: 
            return ("Url non valide", 0)     
        
        self.setupImage(image)
        self.loaded = 0
        return ("Image chargée", 1)
        
    def computeImage(self):
        if(self.loaded != 0):
            return
        try:
            self.loaded = 2
            x = self.drawEnd[0] - self.drawStart[0]
            y = self.drawEnd[1] - self.drawStart[1]
            print(x,y)
            print(self.drawEnd, self.drawStart)
            image = self.image.convert("RGB")
            enhancer = ImageEnhance.Contrast(image)

            image = ImageOps.mirror(image)
            image = image.resize((x,y))

            self.image = np.array(image)
        except:
            self.loaded = 0
            return ("Une erreur est survenue pendant le traitement 1/2", 0)
        return ("Image en cours de traitement 2/2", 1)
        
    def updateColors(self):
        if(self.loaded != 2):
            return
        try:
            self.image = multiProcess(self.image)
        except:
            return ("Une erreur est survenue pendant le traitement 2/2", 0)
        self.loaded = 1
        return ("Image prête", 1)
        
    def selectColor(self, color):
        x,y = self.colorsCoord[color]
        pyautogui.click(x,y)


    def draw(self):  
        if(self.loaded != 1):
            return
        i, j, osef = self.image.shape
        previousColor = (-1, -1, -1)    
        for x in range(0,j,self.compression):
            self.clickMouse(x,0)
            print(x)
            for y in range(0,i,self.compression):
                actualColor = tuple(self.image[y,x])
                if(actualColor != previousColor):
                    previousColor = actualColor
                    self.dragMouse(x,y-1)              
                    self.selectColor(actualColor)
                    self.clickMouse(x,y)
            self.dragMouse(x,i)


@lru_cache()
def giveClosestColor(rgb):
    r, g, b = rgb[:3]
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))

    return min(color_diffs)[1]

def updateColors(pixels, index, return_array):
    i, j, osef = pixels.shape
    for x in range(i):
        for y in range(j):
            pixels[x,y] = giveClosestColor(tuple(pixels[x,y]))

    return_array[index] = pixels


newArray = dict()

def multiProcess(pixels):
    coresCount = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    temp = np.array_split(pixels,coresCount)
   
    processes = []
    for i in range(coresCount):
        array = temp[i]
        p = multiprocessing.Process(target=updateColors, args=(array, i, return_dict))
        processes.append(p)
        p.start()
    
    for process in processes:
        process.join();
        
    
    temp = np.concatenate([v for k,v in sorted(return_dict.items())], 0)
    return temp

                

                
