import urllib.request
import datetime
import sys

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
	
	try:
		unica = urllib.request.urlopen('http://www.unica.fi/fi/ravintolat/'+paikka).read().decode()
		unica = unica.split('h4 data-dayofweek')[1:]
		ret = ''
		while 1:
			htmlsucks = []
			ret += days[paiva] + ': '
			for idx, val in enumerate(unica):
				htmlsucks.append(val.split('class="lunch">')[1:])
			if len(htmlsucks) > paiva:
				for idx, val in enumerate(htmlsucks[paiva]):
					tmp = val.split('\n')
					ret += '| ' + tmp[6].split('/')[0].strip() + ' ' + tmp[0][:-5] + ' |'
			if koko == False:
				break
			paiva += 1
			if len(htmlsucks) <= paiva:
				break
			ret += '\n'
		return ret
	except:
		return 'jotain hajos'
