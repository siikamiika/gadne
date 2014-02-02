import re
import urllib.request
import urllib.parse
import html.parser
import json
import datetime

def desc(url):

    try:
        # collect info from URL
        request = urllib.request.Request(url)
        request.add_header(
            'User-Agent',
            'Mozilla/5.0 '
            '(Windows NT 6.1; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/31.0.1650.57 Safari/537.36')
        response = urllib.request.urlopen(request)
        content_type = response.headers['Content-Type']
        encoding = response.headers.get_content_charset()
        redir = response.geturl()
        ytmatch = re.search('youtube\.com/(?:.*?v=|.*?embed/|.*?v/|/)(.{11})',
            redir)
    except Exception as e:
        if type(e) is not ValueError:
            print(url, e)
        return

    if ytmatch:
        # youtube video info
        try:
            videoid = ytmatch.group(1)
            jsondata = json.loads(urllib.request.urlopen(
                'http://gdata.youtube.com/feeds/api/videos/'+videoid+
                '?v=2&alt=jsonc').read().decode())
            video = jsondata['data']
            kesto = ' ('+str(datetime.timedelta(seconds=video['duration']))+')'
            try:
                likeratio = str(round(
                        (int(video['likeCount'])/video['ratingCount'])*100, 2
                    ))+'%'
            except KeyError:
                likeratio = 'ei ole'
            nippelitieto = ' / '.join([
                    'Aihe: '+video['category'],
                    '{:,}'.format(video['viewCount'])+' katselukertaa',
                    'likeratio: '+likeratio
                ])
            ret = 'Youtube: '
            ret += ('[' + video['uploader'] + '] ' + video['title'] + kesto +
                ' | ' + nippelitieto)
            return ret
        except Exception as e:
            return e

    if 'image/' in content_type.lower():
        try:
            googleimg = ('https://www.google.com/'
                'searchbyimage?&image_url='+urllib.parse.quote(url))
            req = urllib.request.Request(googleimg)
            req.add_header(
                'User-Agent',
                'Mozilla/5.0 '
                '(Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/31.0.1650.57 Safari/537.36')
            result_page = urllib.request.urlopen(req).read()
            match = re.search(b'Best guess for this image.*?>(.*?)</a>',
                result_page, re.M)
            return match.group(1).decode()
        except AttributeError:
            return

    page = response.read(1024*1024)

    if encoding is None:
        charset = (re.search(b'<meta\s[^>]*?(?<=[\s;])charset=\"?([^;\"\s]+)',
            page, re.S | re.I))
        if charset is None:
            encoding = 'utf-8'
        else:
            encoding = charset.group(1).decode()

    title = re.search(b'<title.*?>(.*?)</title>', page, re.S | re.I)
    print('url: {0} redir: {1} encoding: {2} Title: {3}'.format(
        url, redir, encoding, bool(title)
    )) # debug
    if title is None:
        return
    else:
        title = title.group(1).decode(encoding).strip()
        title = html.parser.HTMLParser().unescape(title)
        title = re.sub('\s+', ' ', title)
        return title
