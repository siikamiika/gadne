import urllib.request
import time

def pricediff(h_ago):

    now = urllib.request.urlopen(
        'http://api.bitcoincharts.com/v1/trades.csv?symbol=btceUSD',
        ).readline().decode()
    now = float(now.split(',')[1])

    then = urllib.request.urlopen(
        'http://api.bitcoincharts.com/v1/trades.csv?symbol=btceUSD&start='+
         str(int(time.time() - h_ago*60*60)),
         ).readline().decode()
    then = float(then.split(',')[1])

    if then - now > 0:
        print('hinta laskenut', then-now)
    if then - now < 0:
        print('hinta noussut', now-then)

    #paitsi että listan eka arvo on ~2h sitten...