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

def katse(juuh):
        # Katse se BTC-e API
        if juuh == 'ltc':
            URL = 'ltc_usd'
        elif juuh == 'btc':
            URL = 'btc_usd'
        elif juuh == 'xpm':
            URL = 'xpm_btc'
        URL = 'https://btc-e.com/api/2/{!s}/ticker'.format(URL)
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
        last = 'Iham hyvä 1 {!s} = ${:f}, mitä mieltä muut :rolleyes:'.format(juuh, last)
        # Kuulim :o
        return last
