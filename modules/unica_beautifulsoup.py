import urllib.request
import datetime
import sys
from bs4 import BeautifulSoup
import html5lib

def lounas(paikka, arguments):

	days = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']
	htmldays = ['Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 'Perjantai', 'Lauantai', 'Sunnuntai']
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
	
	try:
		unica = urllib.request.urlopen('http://www.unica.fi/fi/ravintolat/'+paikka).read().decode()
		soppa = BeautifulSoup(unica, 'html5lib')
		menuitems = soppa.find_all('div', {'class':'accord'})
		daystrings = []
		for menuitem in menuitems:
			daystring = ''
			for lunch in menuitem.find_all('tr'):
				daystring += lunch.find("td", {"class":"price quiet"}).next_element.split("Hinta:")[1].split("/")[0].strip()+' '
				daystring += ' | '+lunch.find("td", {"class":"lunch"}).next_element
			daystrings.append(daystring)
	except:
		return 'jotain hajos'
