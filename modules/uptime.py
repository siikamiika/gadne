import datetime

def get(asd):
    try:
        uptime = open('/proc/uptime', 'r').read()
        uptime = float(uptime.split()[0])
        uptime = round(uptime, 0)
        uptime = str(datetime.timedelta(seconds=uptime))
        return uptime
    except Exception as e:
        print(e)
        return
