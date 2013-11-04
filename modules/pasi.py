import re
import urllib.request
import html.parser

def radio():
	try:
		request = urllib.request.Request('http://releet.pasiradio.com:8000/')
		request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5')
		page = urllib.request.urlopen(request).read()
	except:
		return ''
