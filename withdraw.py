#!/usr/bin/python2
import os
import autopy
import time
import grids
import subprocess

# gets initial mouse position to place it back when all functions are finished
cx,cy = autopy.mouse.get_pos()
# boolean to know when itm list window is opened
itmlst_open = False

class mix_Items(object):
    """x,y is the location of the item label in itmlist window, n is the number of items to take out from there"""
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n

        # stores all items before withdrawing any
        store_all()
        # withdraws items 
        grids.itmlst(x,y,n)
        # eats bones 5 times
        grids.inventory(1,n,5)
        # clics mix all button in inventory 
        make_items()



def store_mix_deco(passedfunc):
    """will store all items before withdrawing, then mixing them"""
    def wrapper_function():
        store_all()
        passedfunc()
        make_items()
    return wrapper_function

def move(x,y, repeat):
    """Moves the cursor to x,y and then clicks"""
    #os.system('xdotool mousemove {} {} sleep .1 click --delay 100 --repeat {} 1'.format(x,y, repeat))
    autopy.mouse.move(x,y)
    time.sleep(.1)
    for n in range(repeat):
        autopy.mouse.click(1)


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
    time.sleep(.2)
    move(85,95,times)
    autopy.mouse.click(3)
    time.sleep(.2)
def store_all():
    """Stores all items in inventory"""
    # store all
    move(290,65,1)
    time.sleep(.5)
def get_bones(times):
    # withdraws 10 bones
    for i in xrange(times):
        grids.itmlst(330,120,1)

@store_mix_deco
def make_silver_bars():
    """Takes out by 50 at a time"""
    # takes out silver ore
    grids.itmlst_grid(375,220,3)

def make_items():
    autopy.mouse.click(3)
    ####time.sleep(.3)
    # clicks on the mix all button in inventory
    grids.inventory(5,9,1)

    #moves back to original mouse position
    autopy.mouse.move(cx,cy)

@store_mix_deco
def make_fe():
    grids.itmlst(330,162,3)

@store_mix_deco
def make_ME():
    grids.itmlst(339, 196,5)

    
@store_mix_deco
def make_water_essence():
    # Withdraw BlueStarFlower
    category('Flowers')
    move(484,168,1)
    inbank(1)
    # withdraw BlueLupine 
    move(645,172,1)
    wait()
    inbank(1)
    # Withdraw Sapphire
    category('Minerals')
    move(518,38,1)
    inbank(1)
    wait()
    # withdraw Blue quartz
    move(485,74,1)
    inbank(1)

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
    inbank(1)


def make_HE():
    """moves to passed locx,y, then takes out 2 itmes from there"""
    store_all()
    grids.itmlst(330,180,2)
    get_bones(2)
    make_items()
def make_psr():
    """Makes potions of spirit restorations"""
    store_all()
    grids.itmlst(330,217,5)
    make_items()

def open_console():
    # opens console 
    autopy.key.tap(autopy.key.K_F1)
    time.sleep(8)
    # closes console 
    autopy.key.tap(autopy.key.K_F1)
    time.sleep(.1)


def continuous_make(item_to_make, counter=10):
    # will take out more bones when bones == 0
    bones = 1
    # counter will take out new ings when reaches 0
    # when count reaches 0 break
    count = 50

    item_to_make()
    #opens
    open_console()
    f = '/home/jj/.elc/main/srv_log.txt'
    while True:
        os.system('clear')
        print('counter:',counter)
        print('bones: {}'.format(bones))
        # reads last line of console
        last_line = subprocess.check_output(['tail', '-1', f])
        if count == 0:
            break
        if counter == 0:
            item_to_make()
            open_console()
            counter = 10

        if bones == 0:
            print('Getting Bones')
            get_bones(2)
            bones = 2
        if 'hungry' in last_line:
            print('Hungry, eating')
            make_items()
            time.sleep(1)
            open_console()
            bones -= 1
            print(bones)

        elif 'You failed to'or 'You stopped working' in last_line:
            print('Failed or stopped')
            # click on mix all in man. window
            time.sleep(1)
            autopy.mouse.move(702,478)
            time.sleep(.1)
            autopy.mouse.click(1)

            open_console()

        # closes console if it's open
        counter -= 1
        count -=  1

########################################
#make_fe()
#make_water_essence()
#make_silver_bars()
#make_HE()
#make_psr()
#make_ME()
#mix_ME = mix_Items(339, 196,5)
#mix_EE = mix_Items(330,142,4)
#mix_SilverBars = mix_Items(330,233,4)
#mix_HE = mix_Items(330,180,3)
#mix_IronBars = mix_Items(330,200, 4)
SteelBars = mix_Items(330,270,4)


#print('Move mouse inside window')
#time.sleep(3)
cx,cy = autopy.mouse.get_pos()
#continuous_make(make_HE, 2)

