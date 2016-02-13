import os

triggers = ['!opnum']
HELP = '!opnum [<nick>|set 12345]'

def run(msg):
    msg_args = msg['body'].split()
    storage_path = '{}.opnum'.format(msg['mucnick'])

    if len(msg_args) > 1:
        if msg_args[1] == 'set':
            with open(storage_path, 'w') as f:
                f.write(msg_args[2])
        else:
            nick = msg_args[1]
            if nick + '.opnum' in os.listdir():
                with open(nick+'.opnum') as f:
                    return f.read()
            else:
                return '(not set)'
