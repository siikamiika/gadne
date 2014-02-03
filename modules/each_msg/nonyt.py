import re

def run(msg):
    msg_args = msg['body'].split()
    for a in msg_args:
        if 'nonyt' in ''.join(msg['body'].lower().split()):
            return 'NO NYT :ghammer:'
        if not re.findall('[a-z]|:', msg['body']) and len(re.findall('[A-Z]', msg['body'])) >= 3:
            return ':kasetti:'
        if a.lower().startswith('gnu') or a == ':gnu:':
            return 'hehe gnu gnu'
        if a.lower().startswith('mad') or a == ':mad:':
            return ':kasetti:'
        if a.startswith('läski'):
            return ':laihduta:'
        if a.lower().startswith('feel') or a.lower().startswith('tajuu'):
            return 'Yea, feel me. The beat is all in me.'
    # kaikki hajoo jos tää returni puuttuu dunno why
    return
