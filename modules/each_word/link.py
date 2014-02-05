import re
import urllib.request
import urllib.parse
import html.parser
import json
import zlib
from datetime import timedelta
import html5lib
from bs4 import BeautifulSoup

def run(url):
    """Return info about an url. Statistics for YouTube videos, 
    Google reverse image description for images, 
    post info for MuroBBS/R&T links 
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
        rtmatch = re.search('^http://murobbs.plaza.fi/rapellys-ja-testaus/[0-9]+.*?\.html$', redir)
    except Exception as e:
        if type(e) is not ValueError:
            print(url, e)
        return


    if rtmatch:
        with open('modules/each_word/gadnex.login', 'r') as login:
            usr, pw = login.read().split(':')
        login_url = 'http://murobbs.plaza.fi/login.php?do=login'
        login_headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://murobbs.plaza.fi',
            'Referer': redir,
            'Accept-Encoding': 'gzip,deflate'
        }
        login_data = urllib.parse.urlencode({
                'vb_login_username': usr,
                'vb_login_password': pw,
                'do': 'login'
            }).encode()

        def get_page(cookies):
            rt_headers = dict(login_headers)
            rt_headers.pop('Origin')
            rt_headers['Cookie'] = cookies
            rt_req = urllib.request.Request(redir, headers=rt_headers)
            rt_resp = urllib.request.urlopen(rt_req)
            rt_page = zlib.decompress(rt_resp.read(), 16+zlib.MAX_WBITS)
            return rt_page

        def login():
            login_req = urllib.request.Request(login_url, login_data, login_headers)
            login_resp = urllib.request.urlopen(login_req)
            login_page = zlib.decompress(login_resp.read(), 16+zlib.MAX_WBITS)
            if b'Olet kirjautunut' in login_page:
                print('MuroBBS login success!')
            else:
                print('MuroBBS login failed.')
            cookies = '; '.join(
                    [v.split('; ')[0] for k, v in login_resp.getheaders()
                    if k == 'Set-Cookie']
                )
            with open('modules/each_word/cookies.login', 'w') as c:
                c.write(cookies)
            return cookies

        try:
            with open('modules/each_word/cookies.login', 'r') as c:
                cookies = c.read()
            rt = get_page(cookies)
            if b'Et ole kirjautunut' in rt:
                rt = get_page(login())
            if b'Et ole kirjautunut' in rt:
                return 'Ei voi kirjautua sisään'
        except Exception as e:
            if type(e) == FileNotFoundError:
                rt = get_page(login())
                if b'Et ole kirjautunut' in rt:
                    return 'Ei voi kirjautua sisään'
            else:
                print(e)
                return
        with open('rt.html', 'wb') as f:
            f.write(rt)
        rt = BeautifulSoup(rt.decode('latin-1'), 'html5lib')
        title = rt.title.text.rstrip(' - MuroBBS')
        posts = rt.find_all('table', {'id': re.compile('post[0-9]*')})
        def post_details(post_n):
            return {
                'name': posts[post_n].find('a', {
                    'class': 'bigusername'}).text,

                'time': posts[post_n].find('a', {
                    'name': posts[post_n].get('id')}).img.next.strip(),

                'msg': re.sub('\s+', ' ', ' '.join([
                    (urllib.parse.unquote((child.get('href') or '').replace(
                        'http://murobbs.plaza.fi/redirect-to/?redirect=', ''
                    )) if hasattr(child, 'href') else child) or ''
                    for child in posts[post_n].find(
                        'div', {'id': 'post_message_'+posts[post_n].get('id')[4:]}
                    ).children]))
            }
        print(post_details(0))
        op = post_details(0)
        return '{0} {1} {2}\n{3}'.format(op['name'], op['time'], title, op['msg'])

    elif ytmatch:
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

    elif 'image/' in content_type:
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
    else:
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
