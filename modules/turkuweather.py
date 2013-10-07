import urllib.request
import datetime
import json
import sys

def weather(arguments):
	date = datetime.datetime.now()
	deg = u'\N{DEGREE SIGN}C '
	try:
		delta = int(arguments[0])
		if delta < 0:
			return 'dunnolol'
		date += datetime.timedelta(days=delta)
	except:
		pass
	turku = json.loads(urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q=Turku,fi&mode=json&units=metric').read().decode())
	for weather in turku['list']:
		if datetime.datetime.fromtimestamp(weather['dt']).day == date.day:
			temp = weather['temp']
			ret = date.strftime("%A %d. %B %Y") + ': ' + weather['weather'][0]['description'] + ' | aamu: '+str(temp['morn'])+deg + ' päivä: '+str(temp['day'])+deg + ' ilta: '+str(temp['eve'])+deg + ' yö: '+str(temp['night'])+deg

	return ret