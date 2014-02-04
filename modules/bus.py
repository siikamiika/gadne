import urllib.request
from bs4 import BeautifulSoup

triggers = ['!bus']

def run(msg):
    arguments = msg['body'].split()[1:]
    msgfrom = msg['mucnick']
    if not len(arguments):
        try:
            with open(msgfrom+'.bus', 'r') as favstop:
                stop = str(favstop.read())
        except IOError:
            return 'moi'
    elif arguments[0] == 'fav':
        try:
            with open(msgfrom+'.bus', 'w') as favstop:
                favstop.write(str(arguments[1]))
                stop = arguments[1]
        except:
            return 'moi'
    else:
        stop = arguments[0]

    bussi = urllib.request.urlopen(
            'http://turku.seasam.com/nettinaytto/web'
            '?stopid={}&command=quicksearch&view=mobile'.format(stop)
        ).read().decode('latin-1')
    soppa = BeautifulSoup(bussi)
    ajat = soppa.find('tbody').find_all('tr')[1:]
    retstring = ''
    for aika in ajat:
        retstring += '\n'+aika.find(
            'td', {'class':'timecol'}).next_element.ljust(6)+' | '
        retstring += aika.find(
            'td', {'class':'linecol'}).next_element.ljust(3)+' | '
        retstring += aika.find(
            'td', {'class':'destcol'}).next_element.ljust(20)+'    '
    return retstring
