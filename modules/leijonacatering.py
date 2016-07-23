import urllib.request
from datetime import datetime, timedelta
import sys
from bs4 import BeautifulSoup
import re

triggers = {
    '!rp': '25f04a86-f813-e511-892b-78e3b50298fc',
}
HELP = \
"""
"""
BASEURL = 'http://ruokalistat.leijonacatering.fi/rss/2/'
WEEKDAYS_ABBR = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']

def run(msg):

    msg_args = msg['body'].split()
    paikka = triggers[msg_args[0]]

    date = datetime.now()

    try:
        delta = int(msg_args[1])
        date += timedelta(days=delta)
        paiva = date.weekday()
    except:
        if len(msg_args) > 1:
            if msg_args[1] in WEEKDAYS_ABBR:
                paiva = WEEKDAYS_ABBR.index(msg_args[1])
                date += timedelta(days=(lambda d: d if d >= 0 else d + 7)(paiva - date.weekday()))
        else:
            paiva = date.weekday()

    leijona = urllib.request.urlopen(
            BASEURL+paikka
        ).read().decode()
    soppa = BeautifulSoup(leijona, 'html5lib')
    pvm_re = re.compile(r'.*?(\d+)\.(\d+)\.(\d+).*')
    ateria_re = re.compile(r'(Aamiainen|Lounas|Päivällinen|Iltapala): (.*?)\. ?')
    menuitems = [
        dict(
            pvm=datetime(*[int(d) for d in reversed(pvm_re.match(i.find('title').text).groups())]),
            ateriat=[a for a in ateria_re.findall(i.find('description').text)]
        )
        for i in soppa.find_all('item') if i.find('title').text.strip().endswith('Varusmiesten ruokalista')
    ]
    return (
        ['{}: {}'.format(WEEKDAYS_ABBR[paiva], ' | '.join('{}: {}'.format(a[0], a[1])
            for a in i['ateriat'])) for i in menuitems if i['pvm'].date() == date.date()]
        or [WEEKDAYS_ABBR[paiva] + ': ']
    )[0]
