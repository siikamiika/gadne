import urllib.request
import datetime
from bs4 import BeautifulSoup
import html5lib
from collections import OrderedDict
import json

def lounas(arguments):

    days = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']
    date = datetime.datetime.now()
    #koko = False

    try:
        delta = int(arguments[0])
        date += datetime.timedelta(days=delta)
        paiva = date.weekday()
    except:
        if len(arguments) != 0:
            if arguments[0] in days:
                paiva = days.index(arguments[0])
                date += datetime.timedelta(days=paiva-date.weekday())
            #if arguments[0] == 'koko':
            #    koko = True
            #    paiva = date.weekday()
        else:
            paiva = date.weekday()
    try:
        ict = urllib.request.urlopen('http://www.sodexo.fi/carte/load/html/54/'+str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'/day').read()
        ictfoods = json.loads(ict.decode())
        soppa = BeautifulSoup(ictfoods['foods'], 'html5lib')
        lounaat = soppa.find_all('div', {'class':'lunch_desc inline'})
        hinnat = soppa.find_all('div', {'class':'lunch_price inline'})
        pairs = OrderedDict(zip(lounaat, hinnat))
        rlista = days[paiva]+': '
        for lounas in pairs:
            rlista += '| '+pairs[lounas].find('p').text+' '+lounas.find('span', {'class':'fi title'}).text+' |'

        return rlista

    except:
        return 'jotain hajos'