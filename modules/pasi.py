import re
import urllib.request

def radio():
	try:
		request = urllib.request.Request('http://releet.pasiradio.com:8000/')
		request.add_header('User-Agent', 'Mozilla/5.0 (compatible; gadne; +https://github.com/siikamiika/gadne)')
		page = urllib.request.urlopen(request).read()
		status = re.search(b'Server Status: </font></td><td><font class=default><b>(.*?)</b>', page).group(1).decode()
		if status.startswith('Server is currently up'):
			return 'kuuntele pls http://releet.pasiradio.com:8000/listen.pls'
		elif status.startswith('Server is currently down'):
			return 'striimi alhaalla'
		else:
			return ''
	except:
		return 'errör'
