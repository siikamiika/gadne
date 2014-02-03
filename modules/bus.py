import urllib.request
from bs4 import BeautifulSoup

triggers = ['!bus']

def run(msg):
    arguments = msg['body'].split()[1:]
    msgfrom = msg['mucnick']
    try:
        num = str(int(arguments[0]))
    except ValueError:
        if arguments[0] == 'fav':
            try:
                with open(msgfrom+'.bus', 'w') as favstop:
                    favstop.write(str(int(arguments[1])))
                    num = arguments[1]
            except:
                return 'moi'
    except IndexError:
        try:
            with open(msgfrom+'.bus', 'r') as favstop:
                num = str(int(favstop.read()))
        except IOError:
            return 'moi'
    bussi = urllib.request.urlopen('http://turku.seasam.com/nettinaytto/web?stopid='+num+'&command=quicksearch&view=mobile').read().decode('latin-1')
    soppa = BeautifulSoup(bussi)
    ajat = soppa.find('tbody').find_all('tr')[1:]
    retstring = ''
    for aika in ajat:
        retstring += '\n'+aika.find('td', {'class':'timecol'}).next_element.ljust(6)+' | '
        retstring += aika.find("td", {'class':'linecol'}).next_element.ljust(3)+' | '
        retstring += aika.find('td', {'class':'destcol'}).next_element.ljust(20)+'    '
    return retstring
