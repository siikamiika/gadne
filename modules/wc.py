import re
from collections import Counter

def count(msg):
    viesti = msg['body'][4:]
    try:
        try:
            with open('chatlog.log', 'r') as chatlog:
                chatlog = chatlog.read()
        except UnicodeDecodeError:
            with open('chatlog.log', 'rb') as chatlog:
                chatlog = chatlog.read().decode()
    except IOError:
        return 'ei voi lukea chatlogia'
    rivit = chatlog.split('\n')
    rivit = [ rivi for rivi in rivit if not '!wc' in rivi ]
    chatlog = '\n'.join(rivit)
    nimet = re.findall('(?:'+msg['from'].bare+'/)(.*?)(?:/.*?:\s)(?:.*?)(?:'+re.escape(viesti)+')', chatlog)
    wc = Counter(nimet)
    ret = ''
    for nimi, kerrat in wc.items():
        ret += nimi+': '+str(kerrat)+' '
    return ret
