#/usr/bin/env python
# -*- coding: utf-8 -*-
#
# KATSE SE LTC
# :hammer:
# mää räpeltämäs :gcomp:
# by fisle
#
import urllib2
import simplejson as json

def katse(juuh):
        # Katse se BTC-e API
        if katse == 'ltc':
                URL = 'https://btc-e.com/api/2/ltc_usd/ticker'
        elif katse == 'btc':
                URL = 'https://btc-e.com/api/2/btc_usd/ticker'
        response = urllib2.urlopen(URL)
        html = response.read()
        # Katse se JSON KUULIKKO
        data = json.loads(html)
        last = data['ticker']['last']
        last = 'Iham hyvä 1 {!s} = ${!s}, mitä mieltä muut :rolleyes:'.format(juuh, last)
        # Kuulim :o
        return last
