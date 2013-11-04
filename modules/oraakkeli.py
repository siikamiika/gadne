import urllib.request
import urllib.parse
import re
import sys

site = 'http://www.lintukoto.net/viihde/oraakkeli/index.php'
chromelinux = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5'

req_getrandom = urllib.request.Request(site)
req_getrandom.add_header('User-Agent', chromelinux)
sivu = urllib.request.urlopen(req_getrandom).read()
randomshit = re.search(b'<INPUT NAME=\'(.*?)\'', sivu).group(1).decode('latin-1')
postdata = {
	randomshit:sys.argv[1],
	'submit':'',
	'rnd':randomshit.lstrip('kysymys_')
}
postdata = urllib.parse.urlencode(postdata).encode('latin-1')
print('Debug: '+str(postdata))
req_ask = urllib.request.Request(site, postdata)
req_ask.add_header('User-Agent', chromelinux)
vastaus_raw = urllib.request.urlopen(req_ask).read()
vastaus = re.search(b'<p class=\'vastaus\'>(.*?)</p>', vastaus_raw).group(1).decode('latin-1')
print(vastaus)
