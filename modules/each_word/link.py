import re
import urllib.request
import urllib.parse
import html.parser
import json
from datetime import timedelta

def run(url):
    """Return info about an url. Statistics for YouTube videos, 
    Google reverse image description for images 
    and page title for anything else."""

    # required for reverse image search and possibly other sites
    user_agent = (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/31.0.1650.57 Safari/537.36'
        )

    try:
        # collect info from URL
        request = urllib.request.Request(url)
        request.add_header('User-Agent', user_agent)
        response = urllib.request.urlopen(request)
        content_type = response.headers['Content-Type'].lower()
        encoding = response.headers.get_content_charset()
        redir = response.geturl()
        ytmatch = re.search('youtube\.com/.*?(?:[\?\&]v=|embed/|v/)(.{11})',
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
                'http://gdata.youtube.com/feeds/api/videos/'
                '{}?v=2&alt=jsonc'.format(videoid)).read().decode())
            video = jsondata['data']
            kesto = timedelta(seconds=video['duration'])
            try:
                likeratio = round(
                        (int(video['likeCount'])/video['ratingCount'])*100,
                    2)
            except KeyError:
                likeratio = '0/0'

            print('YouTube:', videoid)
            return ('Youtube: [{0}] {1} ({2}) | Aihe: {3} / '
                '{4:,} katselukertaa / likeratio: {5}%').format(
                    video['uploader'], video['title'], kesto,
                    video['category'], video['viewCount'], likeratio
                )
        except Exception as e:
            print(e)
            return

    if 'image/' in content_type:
        # reverse image search
        try:
            googleimg = ('https://www.google.com/'
                'searchbyimage?&image_url='+urllib.parse.quote(url))
            req = urllib.request.Request(googleimg)
            req.add_header('User-Agent', user_agent)
            result_page = urllib.request.urlopen(req).read()
            imagedesc = re.search(b'Best guess for this image.*?>(.*?)</a>',
                result_page, re.M).group(1).decode()
            print(url, 'img:', imagedesc)
            return imagedesc
        except AttributeError:
            print(url, 'no image description')
            return

    # don't block by downloading page before detecting youtube link or image
    page = response.read(1024*1024)

    if encoding is None:
        # search encoding from meta tag
        charset = (re.search(b'<meta\s[^>]*?(?<=[\s;])charset=\"?([^;\"\s]+)',
            page, re.S | re.I))
        if charset is None:
            # utf-8 fallback
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
