#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:28:37 2021

@author: robinzmuda
"""

from pynput.mouse import Listener
from pynput.mouse import Button

count = 0
start = -1
end = -1

def on_click(x, y, button, pressed):
    if(button == Button.left):
        global count
        if(pressed == True) & (count == 0):
            global start
            start = (x,y)
            count = 1 
        elif(pressed == True):
            global end
            end = (x,y)
            return False
        
def detectClick():
    global count
    count = 0
    with Listener(on_click=on_click) as listener:
        listener.join()
    return start,end
    
