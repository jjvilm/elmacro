#!/usr/bin/python2
import autopy
import time
from modules import InterfaceDetect

def inventory(row,col,clicks):
    """pass row and colum of item to click by n clicks in inventory
    Rows and Colums start at 0
    """
    # ROWS AND COLS START AT 0
    x,y = 18,33
    w = 34
    l = 34
    # row,col iterations
    rite = 0 
    cite = 0
    while True:
        # At target row and col
        if rite == row and cite == col:
            for _ in range(clicks):
                move(x,y)
            break
        else:
            # resets cols, and moves to next row
            if cite == 8:
                rite += 1
                y += l
                cite = 0
                x = 18
            # moves to next colum
            else:
                cite += 1
                x += w
        if rite > 5:
            print('No more rows to iterate')
            break

    """Checks to see if itmlst is open to take out bones"""

def itmlst(loc_x, loc_y,n_items):
    """Pass x,y of items in list to take out.  n_items is the number of item in that list to take out
    last one being bones"""
    # opens itm list if not already open
    InterfaceDetect.open_itmlst_window()
    time.sleep(0.1)
    # moves to ingredients in itmlst location
    move(loc_x, loc_y)
    time.sleep(0.1)

    x,y = 330,30
    w = 34
    l = 30
    for i in range(n_items):
        # moves to item in itmlst, clicks 
        # then moves to bank
        move(x,y)
        inbank()
        x += w
        if i == 5:
            # moves curosor to next row
            y += l
            # resets X coord
            x = 330
        if i == 11:
            # moves curosor to next row
            y += l
            x = 330
    # closes item lst window
    inventory(5,8,1)

def action_btn(button_n):
    """clicks on buttons on the bottom of the game
    buttons range from 1-21"""
    x,y = 16,529
    for i in range(button_n):
        # this makes sures i matches button_n
        i += 1
        if i == button_n:
            move(x,y)
        else:
            x += 32

def category(name):
    """Clicks on the item category"""
    cat = {'Food':0,'Coins':0,'Flowers':(353,69),'Ores':(345,82),'Minerals':(357,109), 'Essences':(357,174),'Animal':(347,199)}
    x, y = cat[name]
    move(x,y)
    wait()

def storage(row,col,repeat):
    """repeat number of times to click"""
    x,y = 486,43
    w = 34
    l = 30
    if row != 1:
        row -= 1
        y = y+(l*row)
    if col != 1:
        col -= 1
        x = x+(w*col)
    move(x,y)
    # Withdraws into bank item
    inbank()

def move(x,y):
    """Moves the cursor to x,y and then clicks"""
    #os.system('xdotool mousemove {} {} sleep .1 click --delay 100 --repeat {} 1'.format(x,y, repeat))
    time.sleep(.03)
    autopy.mouse.move(x,y)
    time.sleep(.07)
    autopy.mouse.click(1)
    time.sleep(.07)

def wait(n=.3):
    """Change to a higher number to compensate for lagg"""
    time.sleep(n)

def inbank():
    """Deposits held item into bank then right clicks"""
    move(85,95)
    wait(.2)
    autopy.mouse.click(3)
    wait(.2)

def store_all():
    """Stores all items in inventory"""
    # store all
    #move(290,65)
    #time.sleep(.2)
    inventory(1,8,1)

def mix_all():
    """Clicks on mix all button in inventory"""
    inventory(4,8,1)
    time.sleep(.05)

if __name__ == "__main__":
    pass
