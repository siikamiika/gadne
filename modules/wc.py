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
    rivit = [rivi for rivi in chatlog.split('\n') if not '!wc' in rivi]
    nimet = re.findall('(?:'+msg['from'].bare+'/)(.*?)(?:/.*?:\s)(?:.*?)(?:'+re.escape(viesti)+')', '\n'.join(rivit))
    wc = Counter(nimet)
    return ', '.join([tup[0]+': '+str(tup[1]) for tup in wc.most_common()])
