from datetime import datetime, timedelta
from modules import unica, sodexo, spam
from threading import Thread

triggers = ['!ruoka']

def run(msg):
    msg_args = msg['body'].split()
    d = datetime.utcnow() + timedelta(hours=2)
    daylist = ['ma', 'ti', 'ke', 'to', 'pe', 'la', 'su']
    delta = 0
    ruokafile = '{}.ruoka'.format(msg['mucnick'])

    if len(msg_args) > 1 and msg_args[1] == 'fav':
        with open(ruokafile, 'w') as f:
            f.write(' '.join([
                r for r in msg_args[2:]
                if r in list(unica.triggers) + ['!ict', '!gadne', '!spam']
            ]))

    try:
        with open(ruokafile, 'r') as f:
            favs = f.read().split()
    except Exception as e:
        return ('valitse lempiravintolat ensin '
               '(!ruoka fav !ict !assari !delica ...)')

    if len(msg_args) == 1 and d.hour >= 16:
        delta = 1
    else:
        try:
            delta = int(msg_args[1])
        except IndexError:
            pass
        except ValueError:
            if msg_args[1] in daylist:
                delta = daylist.index(msg_args[1]) - d.weekday()

    def fuck_unica(paikka, delta):
        ruokalistat.append('{}: '.format(paikka[1:])+unica.run(
            {'body': '{p} {d}'.format(p=paikka, d=delta)}
        ))

    ruokalistat = []
    threads = []
    for paikka in favs:
        if paikka in unica.triggers:
            threads.append(Thread(target=fuck_unica, args=(paikka, delta)))
            threads[-1].start()
        elif paikka == '!ict':
            ruokalistat.append('ict '+
                sodexo.run({'body': '!ict {}'.format(delta)})
            )
        elif paikka == '!gadne':
            ruokalistat.append('gadne: :laihduta:')
        elif paikka == '!spam':
            ruokalistat.append('python: {}'.format(spam.run(msg)))

    for t in threads:
        t.join()
    
    return '\n'.join(ruokalistat)
