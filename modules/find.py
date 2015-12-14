import re

triggers = ['!find', '!rfind', '!efind', '!refind', '!erfind']

def run(cmd):

    c, pattern = (cmd['body'].split(None, 1) + [''])[0:2]

    occurrence = re.match('(\d+) (.*)', pattern) or 0
    if occurrence:
        occurrence, pattern = occurrence.groups()
    else:
        # unescape '\123 message body' to '123 message body'
        if re.match(r'\\\d', pattern):
            pattern = pattern[1:]
    occurrence = int(occurrence)

    opts = cmd['body'][1:3]

    rev = False
    if 'r' in opts:
        rev = True
    if 'e' not in opts:
        pattern = re.escape(pattern)

    pattern = re.compile(pattern)

    with open('chatlog.log', 'rb') as chatlog:
        chatlog = chatlog.read().decode().splitlines()

    if rev:
        chatlog = reversed(chatlog)

    for line in chatlog:
        if [t for t in triggers if t in line]:
            continue

        line = line.split(None, 3) + ['']
        time = ' '.join(line[0:2])
        nick = line[2].split('/')[1]
        msg = line[3]

        if pattern.search(msg):
            if occurrence == 0:
                return '{c}: {time} {nick}: {msg}'.format(**locals())
            else:
                occurrence -= 1
