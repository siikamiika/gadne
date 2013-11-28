import datetime

def get():
    try:
        uptime = open('/proc/uptime', 'r').read()
        uptime = float(uptime.split()[0])
        uptime = round(uptime, 0)
        uptime = str(datetime.timedelta(seconds=uptime))
        return uptime
    except:
        return ''
