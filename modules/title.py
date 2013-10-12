import re
import urllib.request
import html.parser

def get(url):
	try:
		page = urllib.request.urlopen(url).read()
		title = re.search(b'<title.*?>(.*?)</title>', page, re.S | re.I).group(1)
		title = title.decode().strip()
		title = html.parser.HTMLParser().unescape(title)
	except AttributeError:
		return ''
	return title