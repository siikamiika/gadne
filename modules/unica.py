import urllib.request
from datetime import datetime, timedelta
import sys
from bs4 import BeautifulSoup
import html5lib
import re

triggers = {
    '!assari': 'assarin-ullakko/',
    '!tottis': 'tottisalmi/',
    '!delica': 'delica/',
    '!brygge': 'brygge/',
    '!deli': 'deli-pharma/',
    '!dental': 'dental/',
    '!mac': 'macciavelli/',
    '!mikro': 'mikro/',
    '!nutri': 'nutritio/',
    '!rk': 'ruokakello/',
    '!unica': None
}

def run(msg):

    msg_args = msg['body'].split()
    paikka = triggers[msg_args[0]]

    if not paikka:
        return ', '.join(
            '{}: {}'.format(t, v) for t, v in triggers.items()
            if t != '!unica'
        )

    days = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']
    date = datetime.now()
    koko = False

    try:
        delta = int(msg_args[1])
        date += timedelta(days=delta)
        paiva = date.weekday()
    except:
        if len(msg_args) > 1:
            if msg_args[1] in days:
                paiva = days.index(msg_args[1])
        else:
            paiva = date.weekday()
    
    unica = urllib.request.urlopen(
           'http://www.unica.fi/fi/ravintolat/'+paikka
        ).read().decode()
    soppa = BeautifulSoup(unica, 'html5lib')
    week = int(date.strftime('%V'))
    list_week = int(soppa.find('h3', {'class': 'head2'}).text.split()[-1])
    if week != list_week:
        return '{}:'.format(days[paiva])
    menuitems = soppa.find_all('div', {'class':'accord'})
    daystrings = dict((idx, val+':') for idx, val in enumerate(days))
    for menuitem in menuitems:
        day = int(menuitem.find('h4')['data-dayofweek'])
        daystring = days[day]+': '
        for lunch in menuitem.find_all('tr'):
            try:
                daystring += '| '
                daystring += lunch.find(
                        'td', {'class':'price quiet'}
                    ).contents[0].split('Hinta:')[1].split('/')[0].strip()+' '
            except:
                pass
            try:
                daystring += lunch.find(
                        'td', {'class':'lunch'}
                    ).contents[0]+' |'
            except:
                pass
        daystrings[day] = re.sub('\s+', ' ', daystring)
    
    ret = daystrings.get(paiva)
    if 'riisi' in ret.lower():
        ret += ' "Taas riisiä" :grage:'
    return ret

