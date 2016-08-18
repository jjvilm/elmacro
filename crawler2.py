#!/usr/bin/python3
#from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup as bs
from os import system

#url = input("URL:\n")
url = "eternal-lands.com"

url = "https://www."+url
page = requests.get(url)

con = page.content
# gets htlm
soup = bs(con, "html5lib")

#pretty = soup.prettify()
#td = soup.find_all("table")

#######################################
sources = soup.find_all("p")
print(sources)
