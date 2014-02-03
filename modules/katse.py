#/usr/bin/env python
# -*- coding: utf-8 -*-
#
# KATSE SE LTC
# :hammer:
# mää räpeltämäs :gcomp:
# by fisle
#
import urllib.request
import json

triggers = {
    '!btc': 'btc_usd',
    '!ltc': 'ltc_usd',
    '!xpm': 'xpm_btc'
}

def run(juuh):
    juuh = triggers[juuh['body'].split()[0]]
    # Katse se BTC-e API
    URL = 'https://btc-e.com/api/2/{!s}/ticker'.format(juuh)
    gconf = urllib.request.urlopen(URL).read().decode()
    # Katse se JSON KUULIKKO
    data = json.loads(gconf)
    last = data['ticker']['last']
    # Mää laskemassa primecoin->usd =D
    if juuh == 'xpm':
        btc = URL.replace('xpm_btc', 'btc_usd')
        btc = urllib.request.urlopen(btc).read().decode()
        btc = json.loads(btc)
        btc = btc['ticker']['last']
        last = last * btc
    last = 'Iham hyvä {!s} = ${:f}, mitä mieltä muut :rolleyes:'.format(juuh.replace('_', '/'), last)
    # Kuulim :o
    return last
