import re
import urllib.request
import html.parser

def get(url):
    try:
        request = urllib.request.Request(url)
        request.add_header(
            'User-Agent',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) '
            'Chrome/19.0.1084.9 Safari/536.5')
        response = urllib.request.urlopen(request)
        page = response.read(1024*1024)
    except Exception as e:
        return ''
    encoding = response.headers.get_content_charset()
    if encoding is None:
        charset = (
            #yolo
            re.search(b'<meta\s+charset=\"(.*?)\"', page, re.S | re.I) or
            re.search(b'<meta\s+http-equiv=\"content-type\"\s+content=\".*?; charset=(.*?)[\";]', page, re.S | re.I)
        )
        if charset is None:
            encoding = 'utf-8'
        else:
            encoding = charset.group(1).decode()
    print(url, encoding) # debug
    title = re.search(b'<title.*?>(.*?)</title>', page, re.S | re.I).group(1)
    title = title.decode(encoding).strip()
    title = html.parser.HTMLParser().unescape(title)
    title = re.sub('\s+', ' ', title)
    return title
