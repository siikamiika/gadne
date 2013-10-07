import urllib.request,datetime,json,sys

def lounas(arguments):
	days = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']
	date = datetime.datetime.now()
	try:
		delta = int(arguments[0])
		date += datetime.timedelta(days=delta)
	except:
		pass
	ruokalista = json.loads(urllib.request.urlopen('http://www.sodexo.fi/ruokalistat/output/daily_json/427/'+str(date.year)+'/'+str(date.month)+'/'+str(date.day)+'/fi').read().decode())
	ret = days[date.weekday()] + ': '
	for ruoka in ruokalista['courses']:
		ret += '| ' + ruoka['price'].split('/')[0] + ruoka['title_fi'] + ' |'
	return ret