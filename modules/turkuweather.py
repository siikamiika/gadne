import urllib.request
import datetime
import json

def weather(arguments):
	date = datetime.datetime.now()
	deg = '\N{DEGREE SIGN}C '
	try:
		delta = int(arguments[0])
		if delta < 0:
			return 'dunnolol'
		date += datetime.timedelta(days=delta)
	except:
		pass
	turku = json.loads(urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q=Turku,fi&mode=json&units=metric&cnt=14').read().decode())
	ret = 'dunnolol'
	for weather in turku['list']:
		weatherdate = datetime.datetime.fromtimestamp(weather['dt'])
		if weatherdate.day == date.day and weatherdate.month == date.month and weatherdate.year == date.year:
			temp = weather['temp']
			ret = date.strftime("%A %d. %B %Y") + ': ' + weather['weather'][0]['description'] + ' | aamu: '+str(temp['morn'])+deg + ' päivä: '+str(temp['day'])+deg + ' ilta: '+str(temp['eve'])+deg + ' yö: '+str(temp['night'])+deg

	return ret
