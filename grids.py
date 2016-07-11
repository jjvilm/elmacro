#!/usr/bin/python2
import autopy
import time


def move(x,y):
    """Moves the cursor to x,y and then clicks"""
    #os.system('xdotool mousemove {} {} sleep .1 click --delay 100 --repeat {} 1'.format(x,y, repeat))
    autopy.mouse.move(x,y)
    time.sleep(.1)
    autopy.mouse.click(1)


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
    wait(.1)
    autopy.mouse.click(3)
    wait(.1)
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
    # moves to passed location
    move(loc_x, loc_y)
    wait(.5)

    x,y = 330,30
    w = 34
    l = 30
    for i in range(n_items):
        move(x,y)
        inbank()
        x += w
        if i == 7:
            y += l
        if i == 13:
            y += l
    # Withdraws into bank item
    itmlst_toggle()

def inventory(row,col,clicks):
    """pass row and colum of item to click by n clicks in inventory"""
    # old 
    #x,y = 20,27
    # new revised coords
    x,y = 18,33
    w = 34
    l = 34
    if row != 1:
        row -= 1
        y = y+(l*row)
    if col != 1:
        col -= 1
        x = x+(w*col)

    #click on the use button before clicking bones
    move(110,528)
    autopy.mouse.move(x,y)
    time.sleep(.1)
    for i in range(clicks):
        autopy.mouse.click(1)
        time.sleep(.01)
    time.sleep(.1)

def itmlst_toggle():
    """Checks to see if itmlst is open to take out bones"""
    # opens/closes itm lst
    move(295,200)
    wait()



if __name__ == "__main__":
    inventory(1,3,5)
