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

    request_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                  'q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-US,en;q=0.8,fi;q=0.6',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/31.0.1650.57 Safari/537.36'
    }   # aka why user-agent filtering doesn't work
        # and who could resist Gadne anyway? :-)

    try:
        # collect info about URL
        request = urllib.request.Request(url, headers=request_headers)
        response = urllib.request.urlopen(request, timeout=10)
        content_type = response.headers['Content-Type'].lower()
        encoding = response.headers.get_content_charset()
        redir = response.geturl()
        ytmatch = re.search('youtube\.com/.*?(?:[\?\&]v=|embed/|v/)(.{11})',
            redir)
        rtmatch = re.search(
            '^http://murobbs.plaza.fi/rapellys-ja-testaus/'
            '[0-9]+.*?\.html', redir)
    except Exception as e:
        if type(e) is not ValueError:
            print(url, e)
        return

    def decompress(data):
        try:
            if data[:2] == b'\x1f\x8b':
                return zlib.decompress(data, 16+zlib.MAX_WBITS)
            else:
                return data
        except Exception as e:
            print(e)
            return data

    def revimg(url):
        try:
            googleimg = ('https://www.google.com/'
                'searchbyimage?&image_url='+urllib.parse.quote(url))
            req = urllib.request.Request(googleimg, headers=request_headers)
            result_page = urllib.request.urlopen(req, timeout=10).read()
            result_page = decompress(result_page)
            imagedesc = re.search(b'Best guess for this image.*?>(.*?)</a>',
                result_page, re.M).group(1).decode()
            return imagedesc
        except AttributeError:
            print(url, 'no image description')
            return
        except Exception as e:
            print(url, e)
            return

    if rtmatch:
        # nyt on tuuhea skenaario
        with open('modules/each_word/gadnex.login', 'r') as login:
            try:
                usr, pw = login.read().split(':')
            except Exception as e:
                print('Error reading username and password:', e)
                return
        if '#' in url:
            # ja se defaultti posts/page päälle tai tulee rumaa jälkeä
            post_id = url[1+url.index('#'):]
            # KUULIKKO
        else:
            # defaulttaa ensimmäiseen viestiin
            post_id = ''
        login_url = 'http://murobbs.plaza.fi/login.php?do=login'
        login_headers = dict(request_headers)
        login_headers['Content-Type'] = 'application/x-www-form-urlencoded'
        login_headers['Origin'] = 'http://murobbs.plaza.fi'
        login_data = urllib.parse.urlencode({
                'vb_login_username': usr,
                # moi NSA mun passu on ***** mitäs mieltä
                'vb_login_password': pw,
                'do': 'login'
            }).encode('windows-1252', 'ignore')

        def get_page(cookies):
            rt_headers = dict(request_headers)
            rt_headers['Cookie'] = cookies
            try:
                rt_req = urllib.request.Request(redir, headers=rt_headers)
                rt_resp = urllib.request.urlopen(rt_req)
                rt_page = decompress(rt_resp.read())
                return rt_page
            except Exception as e:
                print(e)
                return

        def login():
            try:
                login_req = urllib.request.Request(
                    login_url, login_data, login_headers)
                login_resp = urllib.request.urlopen(login_req)
                login_page = decompress(login_resp.read())
            except Exception as e:
                print(e)
                return
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
            if not rt:
                return 'Ei voi ladata sivua'
            elif b'Et ole kirjautunut' in rt:
                rt = get_page(login())
            if b'Et ole kirjautunut' in rt:
                return 'Ei voi kirjautua sisään'
        except Exception as e:
            if type(e) == OSError or IOError:
                rt = get_page(login())
                if not rt:
                    return 'Ei voi ladata sivua'
                elif b'Et ole kirjautunut' in rt:
                    return 'Ei voi kirjautua sisään'
            else:
                print(e)
                return

        try:
            rt = BeautifulSoup(rt.decode('windows-1252'), 'html5lib')
        except Exception as e:
            print(e)
            # ei se mikää tärkee merkki ollu :ghammer:
            rt = BeautifulSoup(
                rt.decode('windows-1252', 'ignore'), 'html5lib')
        title = re.sub('\s+', ' ', rt.title.text.strip()[:-len(' - MuroBBS')])
        posts = rt.find_all('table', {'id': re.compile('post[0-9]*')})
        if not posts:
            # fallback
            return str(title)

        def post_details(post_n):
            sm_path = 'modules/each_word/smilies.json'
            try:
                with open(sm_path, 'r') as s:
                    smilies = json.loads(s.read())
            except Exception as e:
                if type(e) == OSError or IOError:
                    with open(sm_path, 'w') as s:
                        smilies = dict(
                            (s.get('src'), s.get('alt')) for s in
                            BeautifulSoup(
                                urllib.request.urlopen(
                                    'http://murobbs.plaza.fi/misc.php'
                                    '?do=getsmilies').read().decode(
                                    'windows-1252')
                                )
                            .find_all(
                                    'img',{'id': re.compile('smilie_')}
                                )
                            )
                        s.write(json.dumps(smilies))
                else:
                    return 'hymiöissä vikaa :mad:'

            post_msg = []

            for item in posts[post_n].find(
                    'div', {'id': 'post_message_'+posts[post_n].get('id')[4:]}
                ).children:

                if hasattr(item, 'get') and item.get('href'):
                    # markdown much
                    post_msg.append('[{0}]({1})'.format(item.text,
                        urllib.parse.unquote(item.get('href')).replace(
                            'http://murobbs.plaza.fi/redirect-to/?redirect=',
                            ''
                        )))
                if hasattr(item, 'get') and item.get('src'):
                    src = item.get('src')
                    smilie = src.replace('http://murobbs.plaza.fi/', '')
                    if smilie in smilies:
                        # :gcomp:
                        post_msg.append(smilies[smilie])
                    else:
                        # img alt filled with reverse image result
                        post_msg.append('![{0}]({1})'.format(
                            revimg(src) or '', src))
                # the "just text" inside the div
                if item.name is None:
                    msg_len = len(' '.join(post_msg))
                    # limit message length to 300 chars + links/images
                    if msg_len <= 300:
                        post_msg.append(str(item)[:(300-msg_len)])
                    else:
                        post_msg.append('...')

            return {
                'name': posts[post_n].find('a', {
                    'class': 'bigusername'}).text,

                'time': posts[post_n].find('a', {
                    'name': posts[post_n].get('id')}).img.next.strip(),

                'msg': re.sub('\s+', ' ', ' '.join(post_msg).strip())
            }

        try:
            p_ids = [p.get('id') for p in posts]
            p = post_details(p_ids.index(post_id) if post_id in p_ids else 0)
        except Exception as e:
            print(e)
            return
        return '{0} {1} {2}\n{3}'.format(
                p['name'], p['time'], title, p['msg']
            )

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
                # key not found = no likes/dislikes yet
                likeratio = '0/0'

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
        return revimg(url)

    else:
        try:
            page = decompress(response.read(1024*1024))
        except Exception as e:
            print(url, e)
            return

        if not encoding:
            # search encoding from meta http-equiv and meta charset
            charset = (re.search(
                    b'<meta\s[^>]*?(?<=[\s;])charset=\"?([^;\"\s]+)',
                page, re.S | re.I))
            if charset:
                try:
                    encoding = charset.group(1).decode()
                except Exception as e:
                    print(e)

        title = re.search(b'<title.*?>(.*?)</title>', page, re.S | re.I)
        if title is None:
            return
        else:
            title = title.group(1)
            try:
                title = title.decode(encoding)
            except Exception as e:
                print(url, e)
                # fuck you shitty site
                title = title.decode('utf-8', 'ignore')
            title = html.parser.HTMLParser().unescape(title.strip())
            title = re.sub('\s+', ' ', title)
            return title
