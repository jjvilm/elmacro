#!/usr/bin/python2
import autopy
import time
from contMake import itmlst_window


def move(x,y):
    """Moves the cursor to x,y and then clicks"""
    #os.system('xdotool mousemove {} {} sleep .1 click --delay 100 --repeat {} 1'.format(x,y, repeat))
    time.sleep(.01)
    autopy.mouse.move(x,y)
    time.sleep(.05)
    autopy.mouse.click(1)
    time.sleep(.05)


def wait(n=.3):
    """Change to a higher number to compensate for lagg"""
    time.sleep(n)

def category(name):
    """Clicks on the item category"""
    cat = {'Food':0,'Coins':0,'Flowers':(353,69),'Ores':(345,82),'Minerals':(357,109), 'Essences':(357,174),'Animal':(347,199)}
    x, y = cat[name]
    move(x,y)
    wait()

def inbank():
    """Deposits held item into bank then right clicks"""
    move(85,95)
    wait(.2)
    autopy.mouse.click(3)
    wait(.2)
def store_all():
    """Stores all items in inventory"""
    # store all
    move(290,65)
    time.sleep(.2)

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

def itmlst(loc_x, loc_y,n_items):
    #opens itm list
    itmlst_toggle()
    # moves to ingredients in itmlst location
    move(loc_x, loc_y)

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
    # Withdraws into bank item
    itmlst_toggle()

def inventory(row,col,clicks):
    """pass row and colum of item to click by n clicks in inventory"""
    # clicks on the walk icon to be able to equipt items
    move(15,530)
    # ROWS AND COLS START AT 0
    x,y = 18,33
    w = 34
    l = 34
    # row,col iterations
    rite = 0 
    cite = 0
    while True:
        if rite == row and cite == col:
            for _ in range(clicks):
                move(x,y)
            break
        else:
            if cite == 5:
                rite += 1
                y += l
                cite = 0
                x = 18
            else:
                cite += 1
                x += w
        if rite > 5:
            break

def itmlst_toggle():
    """Checks to see if itmlst is open to take out bones"""
    itmlst_window()

if __name__ == "__main__":
    inventory(1,3,5)
