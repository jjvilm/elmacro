#!/usr/bin/python2
import os
import autopy
import time
import grids
import subprocess

# gets initial mouse position to place it back when all functions are finished
# boolean to know when itm list window is opened
itmlst_open = False

class mix_Items(object):
    """x,y is the location of the item label in itmlist window, n is the number of items to take out from there"""
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n

    def run(self):
        # stores all items before withdrawing any
        store_all()
        # withdraws items 
        grids.itmlst(self.x,self.y,self.n)
        self.eat()
        # clics mix all button in inventory 
        mix_all()

    def eat(self):
        # n == last slot where bones reside
        # eats bones 5 times
        grids.inventory(1,self.n,5)

def move(x,y, repeat):
    """Moves the cursor to x,y and then clicks"""
    #os.system('xdotool mousemove {} {} sleep .1 click --delay 100 --repeat {} 1'.format(x,y, repeat))
    autopy.mouse.move(x,y)
    time.sleep(1)
    for n in range(repeat):
        autopy.mouse.click(1)
        time.sleep(.001)
    time.sleep(1)

def wait():
    """Change to a higher number to compensate for lagg"""
    time.sleep(.3)

def category(name):
    """Clicks on the item category"""
    cat = {'Food':0,'Coins':0,'Flowers':(353,69),'Ores':(345,82),'Minerals':(357,109), 'Essences':(357,174),'Animal':(347,199)}
    x, y = cat[name]
    move(x,y,1)
    wait()

def inbank(times):
    """Deposits held item into bank then right clicks"""
    time.sleep(1)
    move(85,95,times)
    time.sleep(1)
    autopy.mouse.click(3)
    time.sleep(1)

def store_all():
    """Stores all items in inventory"""
    # store all
    move(290,65,1)
    time.sleep(.5)

def get_bones(times):
    # withdraws 10 bones
    for i in xrange(times):
        grids.itmlst(330,120,1)

def mix_all():
    #autopy.mouse.click(3)
    ####time.sleep(.3)
    # clicks on the mix all button in inventory
    grids.inventory(5,9,1)

def storage_grid(row,col,repeat):
    x,y = 486,43
    w = 34
    l = 30
    if row != 1:
        row -= 1
        y = y+(l*row)
    if col != 1:
        col -= 1
        x = x+(w*col)
    move(x,y,1)
    # Withdraws into bank item
    inbank(repeat)

def itmlst_grid(row,col):
    # opens list grid
    x,y = 330,30
    w = 34
    l = 30
    if row != 1:
        row -= 1
        y = y+(l*row)
    if col != 1:
        col -= 1
        x = x+(w*col)
    move(x,y,1)
    # Withdraws into bank item
    time.sleep(.07)
    inbank(1)

def mix_dict(item):
    """runs the withdraw process, and mix.  Lastly returns the position of the bones"""
    items = {
        "ME":mix_Items(339, 234,5),
        "EE":mix_Items(330,142,4),
        "silverBar":mix_Items(330,269,4),
        "HE": mix_Items(330,197,3),
        "ironBar": mix_Items(330,214, 4),
        "steelBar": mix_Items(330,286,4),
        "vial": mix_Items(330,307,4),
        "PSR": mix_Items(330,250,6)

    }
    x_instance = items[item]

    return x_instance


########################################
if __name__ == "__main__":
    mix_dict('PSR')
    cx,cy = autopy.mouse.get_pos()

