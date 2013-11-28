import re
import urllib.request
import html.parser

def get(url):
    try:
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5')
        page = urllib.request.urlopen(request).read(1024*1024)
        title = re.search(b'<title.*?>(.*?)</title>', page, re.S | re.I).group(1)
        title = title.decode().strip()
        title = html.parser.HTMLParser().unescape(title)
        return title
    except:
        return ''
