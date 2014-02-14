import datetime
from urllib.request import urlopen

triggers = ['!uptime']

def run(msg):
    uptime_ = False
    target = msg['body'].split()
    if len(target[1:]):
        if target[1] == 'eddykk':
            uptime_ = urlopen('https://eddykaykay.pw/uptime_gadne.php').read()
    try:
        if uptime_:
            uptime = uptime_
        else:
            uptime = open('/proc/uptime', 'r').read()
        uptime = float(uptime.split()[0])
        uptime = round(uptime, 0)
        uptime = str(datetime.timedelta(seconds=uptime))
        return uptime
    except Exception as e:
        print(e)
        return
