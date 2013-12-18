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
        URL = 'https://btc-e.com/api/2/ltc_usd/ticker'
    elif juuh == 'btc':
        URL = 'https://btc-e.com/api/2/btc_usd/ticker'
    gconf = urllib.request.urlopen(URL).read().decode()
    # Katse se JSON KUULIKKO
    data = json.loads(gconf)
    last = data['ticker']['last']
    last = 'Iham hyvä 1 {!s} = ${!s}, mitä mieltä muut :rolleyes:'.format(juuh, last)
    # Kuulim :o
    return last
