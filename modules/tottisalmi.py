import urllib.request
import datetime
import sys

def lounas(arguments):

	days = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']
	date = datetime.datetime.now()

	try:
		delta = int(arguments[0])
		date += datetime.timedelta(days=delta)
		paiva = date.weekday()
	except:
		if len(arguments) != 0:
			if arguments[0] in days:
				paiva = days.index(arguments[0])
		else:
			paiva = date.weekday()
	
	try:
		tottis = urllib.request.urlopen('http://www.unica.fi/fi/ravintolat/tottisalmi/').read().decode()
		tottis = tottis.split('h4 data-dayofweek')[1:]
		yodawg = []
		ret = days[paiva] + ': '
		for idx, val in enumerate(tottis):
			yodawg.append(val.split('class="lunch">')[1:])
		if len(yodawg) > paiva:
			for idx, val in enumerate(yodawg[paiva]):
				tmp = val.split('\n')
				ret += '| ' + tmp[6].split('/')[0].strip() + ' ' + tmp[0][:-5] + ' |'
		return ret
	except:
		return 'jotain hajos'
