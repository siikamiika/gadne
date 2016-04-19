import re
import html5lib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

triggers = ['!incafe']

def run(msg):
    arguments = msg['body'].split()[1:]

    days = ['ma', 'ti', 'ke', 'to', 'pe']
    longDays = ['Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 'Perjantai']
    day = None

    try:
        delta = int(arguments[0])
        then = datetime.now() + timedelta(days=delta)
        day = then.weekday()
    except:
        if len(arguments) != 0:
            if arguments[0] in days:
                day = days.index(arguments[0])
        else:
            day = datetime.now().weekday()

    if day is None:
        return 'anna päivä kuulikko'

    try:
        source = urllib.request.urlopen('http://www.incafe.fi/2').read().decode('ISO-8859-1')
        soup = BeautifulSoup(source, 'html5lib')
        header = soup.find('h2', text=longDays[day]).find_parent('div', class_='madpages_component ksk_no_margins')
        menu = header.find_next_sibling('div', class_='madpages_component ksk_no_margins').table
        courses = []
        for course in menu('tr'):
            title = None
            hasPrice = False
            for el in course('td'):
                s = ' '.join(el.stripped_strings)
                if not s or s.startswith('Otsikko'):
                    continue
                if re.search(r'\d+,\d+', s):
                    hasPrice = True
                    break
                title = s
            if title and not hasPrice:
                courses.append(re.sub(r'\s*([GLM],\s*)*[GLM]\s*$', '', title))
        return days[day] + ': ' + ', '.join(courses)
    except:
        return 'jotain hajos'
