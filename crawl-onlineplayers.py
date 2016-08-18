#!/usr/bin/python3
#from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup as bs
from os import system


url = "http://game.eternal-lands.com/online_players.htm"
page = requests.get(url)

#soup = bs(page.read(), "html.parser")
#soup = bs(page.read())
con = page.content

soup = bs(con, "html5lib")
#pretty = soup.prettify()
n_players = soup.find_all('b' )
n_players = n_players[0].text

# gets the acutal int number
n_play = int(n_players[10:13])

player = soup.find_all('a')

for i,character in enumerate(player):
    if i == n_play:
        break
    print(character.text)

print(n_players)
#######################################


