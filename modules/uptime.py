import datetime

triggers = ['!uptime']

def run(msg):
    try:
        uptime = open('/proc/uptime', 'r').read()
        uptime = float(uptime.split()[0])
        uptime = round(uptime, 0)
        uptime = str(datetime.timedelta(seconds=uptime))
        return uptime
    except Exception as e:
        print(e)
        return
