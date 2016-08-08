#!/usr/bin/python3
#from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup as bs
from os import system

action = str(input("[BUY] or [SELL]\n"))
action = action.capitalize()
#action = 'Sell'
item = str(input("Item?\n"))
item = item.lower()
#item = 'sulfur'

page = requests.get("http://greypal.el-fd.org/cgi-bin/querybot?action={0}&antisocial=1&item={1}&sets=".format(action, item.replace(" ", "+")))

#soup = bs(page.read(), "html.parser")
#soup = bs(page.read())
con = page.content

soup = bs(con, "html5lib")
#pretty = soup.prettify()
td = soup.find_all("table")
def first_bot():
    info = ""
    for i,client in enumerate(td[0].find_all('tr')[1]):
        if i == 1:
            info += client.text+" "
        if i == 3:
            info += client.text+" "
        if i == 5:
            info += client.text+" "
        if i == 6:
            info += client.text+" "
    system('clear')
    print("Who to {} from:\n".format(action))
    print(info)
#######################################
def first_table():
    global td, item
    system("clear")
    # gets the second table which we want
    #td = td[0]
    prices = ""
    counter = 0

    #gets the min avg max prices
    for heading in td[0].find_all('tr'):
        prices = ""
        if counter < 5:
            for i,data in enumerate(heading.find_all('td')):
                # bot
                if i == 1:
                    prices += data.text+"\t"
                # location
                if i == 3:
                    prices += "Loc: "+data.text
                # Amount
                if i == 5:
                    prices += "\nAmount: "+data.text+"\t"
                # price
                if i == 6:
                    prices += "Price: "+data.text.strip()+" "
                # item
                if i == 7:
                    prices += data.text
                    #print(data.text, item.title())
                    #if data.text != item.title():
                    #    prices += ""
                    #    counter = 0
                    #else:
                    #    continue
        else:
            break
        print(prices)
        counter += 1

def second_table():
    global td
    #system("clear")
    # gets the second table which we want
    #td = td[1]
    prices = {}
    counter = 0

    start_adding = False
    #gets the min avg max prices
    for heading in td[1].find_all('tr'):
        for data in heading.find_all('td'):
            if data.text == item.title():
                start_adding = True
            if start_adding:
                if counter == 4:
                    break
                prices[counter] = data.text
                counter += 1
    print("{} {} {} {}".format(prices[0], prices[1], prices[2],prices[3]))

    minimump = float(prices[1][:-2])
    averagep = float(prices[2][:-2])
    maximump = float(prices[3][:-3])
    print("{0:.2f}".format((minimump + averagep + maximump)/3))

first_table()
second_table()
