"""
Extract "Best guess for this image" from Google
reverse image search.

example:

Python 3.3.3
>>> import revimg
>>> revimg.desc('http://static.iltalehti.fi/kuvat/navi/logo_iso.gif')
'iltalehti'

"""
import urllib.request
import urllib.parse
import re

def desc(img):
	desc = ''
	try:
		url = ('https://www.google.com/'
              'searchbyimage?&image_url='+urllib.parse.quote(img)
              )
		req = urllib.request.Request(url)
		#impersonate Google Chrome on Windows 7 to get a proper result page
		req.add_header('User-Agent',
                      ('Mozilla/5.0 '
                       '(Windows NT 6.1; WOW64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/31.0.1650.57 Safari/537.36'))
		page = urllib.request.urlopen(req).read()
		match = re.search(b'Best guess for this image.*?>(.*?)</a>',
                          page, re.M) # keep newlines in same match
		#if there's no description an empty sting will be returned
		desc = match.group(1).decode()
	except AttributeError:
		pass
	return desc
