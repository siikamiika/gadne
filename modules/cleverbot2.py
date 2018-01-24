import sys
from urllib.parse import urlencode
from hashlib import md5
from time import time
from io import StringIO
import re
import requests

triggers = ['gadne:']

class Cleverbot(object):

    HOST = 'www.cleverbot.com'
    PROTOCOL = 'http'
    RESOURCE = '/webservicemin'
    API_URL = '{}://{}{}'.format(PROTOCOL, HOST, RESOURCE)

    TIMEOUT = 5 * 60

    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'

    # TODO: CBSTATE (cookie)
    # TODO: CBALT (cookie)
    # TODO: last_reply_time (query string argument t)

    def __init__(self, debug=False):
        self.session = requests.Session()
        self._set_default_headers()
        self._get_index()
        self._set_cookie('_cbsid', '-1')
        self.last_reply_time = -1
        self.request_count = 0
        self.message_history = []

        self.last_input = ''
        self.last_response = ''

        self.cb_conv_id = ''
        self.xai_prefix = ''
        self.xai_body = ''

        self.language = 'en'

        self.first = True

        self.debug = debug

    def expired(self):
        return (int(time() * 1000) - self.last_reply_time) > self.TIMEOUT * 1000

    def ask(self, text):
        if self.first:
            self.language = self._detect_language(text)
            request_url = '{}?uc=UseOfficialCleverbotAPI&'.format(self.API_URL) # no I won't
        else:
            if self.language == 'en':
                self.language = self._detect_language(text)
            request_url = self._make_request_url(text)

        if self.debug:
            print(request_url, file=sys.stderr)

        request_body = self._make_post_request_body(text)
        if self.debug:
            print(request_body, file=sys.stderr)
        post_response = self.session.post(request_url, data=request_body)
        self.request_count += 1
        self.message_history.append(text)
        self.last_input = text

        response_data = post_response.content.decode('utf-8').splitlines()
        self.message_history.append(response_data[0])
        self.last_response = response_data[0]
        self.cb_conv_id = response_data[1]

        if self.first:
            self._set_cookie('CBSID', self.cb_conv_id)
            self.xai_prefix = self.session.cookies.get('XAI')
            # GET
            get_url = self._make_request_url(text)
            self.session.get(get_url)
            self.request_count += 1

        self.xai_body = response_data[2]

        self.last_reply_time = int(time() * 1000)
        self.first = False

        return self.last_response

    def _set_default_headers(self):
        self.session.headers.update({
            'User-Agent': self.USER_AGENT,
        })

    def _get_index(self):
        """Sets the XVIS cookie"""
        self.session.get('{}://{}/'.format(self.PROTOCOL, self.HOST))

    def _set_cookie(self, name, value):
        self.session.cookies.set(name, value, domain=self.HOST, path='/')

    def _encode_text_for_message(self, text):
        result = StringIO()
        text = text.replace('|', '{*}')
        for c in text:
            if ord(c) > 0xff:
                result.write('|{:04x}'.format(ord(c)))
            else:
                result.write(c)

        return result.getvalue()

    def _format_text(self, text):
        text = list(text)
        if text:
            text[0] = text[0].upper()
            if text[-1] not in ['.', '!', '?']:
                text.append('.')
        return ''.join(text)

    def _detect_language(self, text):
        lang = 'en'

        if 'ä' in text or 'ö' in text:
            lang = 'fi'
        elif 'å' in text:
            lang = 'sv'
        elif re.search(u'[\u0400-\u04FF]', text):
            lang = 'ru'
        elif re.search(u'[\u3041-\u309F\u30A1-\u30FA]', text):
            lang = 'ja'
        elif re.search(u'[\uAC00-\uD7A3]', text):
            lang = 'ko'
        elif re.search(u'[\u2E80-\u2FD5\u3400-\u4DBF\u4E00-\u9FCC]', text):
            lang = 'zh'

        if self.debug:
            print(lang, file=sys.stderr)

        return lang

    def _make_request_url(self, text):
        data = [
            ('uc', 'UseOfficialCleverbotAPI'), # nope, still not convinced
            ('out', self._format_text(self.last_response)),
            ('in', self._format_text(text)),
            ('bot', 'c'),
            ('cbsid', self.cb_conv_id),
            ('xai', self.xai_prefix + ',{}'.format(self.xai_body) * bool(self.xai_body)),
            ('ns', self.request_count),
            ('al', ''),
            ('dl', ''),
            ('flag', ''),
            ('user', ''),
            ('mode', 1),
            ('alt', 0),
            ('reac', ''),
            ('emo', ''),
            ('sou', ''),
            ('xed', ''),
        ]

        return '{}?{}'.format(self.API_URL, urlencode(data))

    def _make_post_request_body(self, text):
        data = [
            ('stimulus', self._format_text(self._encode_text_for_message(text))),
        ]
        data += [('vText{}'.format(i + 2), self._format_text(self._encode_text_for_message(m)))
                 for i, m in enumerate(reversed(self.message_history))]
        data += [
            ('cb_settings_language', self.language),
            ('cb_settings_scripting', 'no'),
            ('sessionid', self.cb_conv_id),
            ('islearning', '1'),
            ('icognoid', 'wsf'),
        ]

        icognocheck = urlencode(data)[7:33].encode('utf-8')
        icognocheck = md5(icognocheck).hexdigest()

        data.append(('icognocheck', icognocheck))

        return data


def run(msg, cleverbot=None):
    msg = msg['body'][len('gadne: '):]
    if not cleverbot:
        cleverbot = Cleverbot()
    elif cleverbot.expired():
        cleverbot = Cleverbot()
    return cleverbot.ask(msg), cleverbot
