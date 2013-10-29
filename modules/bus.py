import urllib.request
from bs4 import BeautifulSoup

def aikataulu(num):
	try:
		num = num[0]
		int(num)
		bussi = urllib.request.urlopen('http://turku.seasam.com/nettinaytto/web?stopid='+num+'&command=quicksearch&view=mobile').read().decode('latin-1')
		soppa = BeautifulSoup(bussi)
		ajat = soppa.find('tbody').find_all('tr')[1:]
		retstring = ''
		for aika in ajat:
			retstring += '\n'+aika.find('td', {'class':'timecol'}).next_element.ljust(6)+' | '
			retstring += aika.find("td", {'class':'linecol'}).next_element.ljust(3)+' | '
			retstring += aika.find('td', {'class':'destcol'}).next_element.ljust(20)+'    '
		return retstring
	except:
		return 'moi'
