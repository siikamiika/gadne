import re
from collections import Counter

triggers = ['!wc']


def run(msg):
    viesti = msg['body'][4:]
    try:
        with open('chatlog.log', 'rb') as chatlog:
            chatlog = chatlog.read().decode()
    except IOError:
        return 'ei voi lukea chatlogia'
    rivit = [rivi for rivi in chatlog.split('\n') if '!wc' not in rivi]
    nimet = re.findall(
        '(?<=\/)(\w{3,})(?=\/)(?:.*)(?:' +
        re.escape(viesti)+')', '\n'.join(rivit)
        )
    wc = Counter(nimet)
    return ', '.join([tup[0]+': '+str(tup[1]) for tup in wc.most_common()])
