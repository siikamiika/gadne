import urllib.request
import datetime
import sys
from bs4 import BeautifulSoup
import html5lib
import re

def lounas(paikka, arguments):

    days = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']
    date = datetime.datetime.now()
    koko = False

    try:
        delta = int(arguments[0])
        date += datetime.timedelta(days=delta)
        paiva = date.weekday()
    except:
        if len(arguments) != 0:
            if arguments[0] in days:
                paiva = days.index(arguments[0])
            if arguments[0] == 'koko':
                koko = True
                paiva = date.weekday()
        else:
            paiva = date.weekday()
    
    unica = urllib.request.urlopen('http://www.unica.fi/fi/ravintolat/'+paikka).read().decode()
    soppa = BeautifulSoup(unica, 'html5lib')
    menuitems = soppa.find_all('div', {'class':'accord'})
    daystrings = []
    for idx, menuitem in enumerate(menuitems):
        daystring = days[idx]+': '
        for lunch in menuitem.find_all('tr'):
            try:
                daystring += '| '
                hinta = lunch.find("td", {"class":"price quiet"}).contents[0].split("Hinta:")[1].split("/")[0].strip()
                daystring += re.sub('\n|\t', '', hinta)+' '
            except:
                pass
            try:
                daystring += lunch.find("td", {"class":"lunch"}).contents[0]+' |'
            except:
                pass
        daystrings.append(daystring)
    while len(daystrings) < len(days):
        daystrings.append(days[len(daystrings)]+': ')
    return daystrings[paiva]
