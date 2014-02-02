import urllib.request
import datetime
import sys
from bs4 import BeautifulSoup
import html5lib
import re

def lounas(msg):

    days = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']
    date = datetime.datetime.now()
    koko = False

    try:
        delta = int(msg[1])
        date += datetime.timedelta(days=delta)
        paiva = date.weekday()
    except:
        if len(msg) > 1:
            if msg[1] in days:
                paiva = days.index(msg[1])
        else:
            paiva = date.weekday()
    
    unica = urllib.request.urlopen('http://www.unica.fi/fi/ravintolat/'+msg[0]).read().decode()
    soppa = BeautifulSoup(unica, 'html5lib')
    menuitems = soppa.find_all('div', {'class':'accord'})
    daystrings = dict((idx, val+':') for idx, val in enumerate(days))
    for menuitem in menuitems:
        day = int(menuitem.find('h4')['data-dayofweek'])
        daystring = days[day]+': '
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
        daystrings[day] = daystring

    return daystrings.get(paiva)
