import re

triggers = ['!wc', '!ewc']

def run(cmd):

    pattern = cmd['body'].split(maxsplit=1)
    if len(pattern) > 1:
        pattern = pattern[1]
    else:
        pattern = ''

    try:
        with open('chatlog.log', 'rb') as chatlog:
            chatlog = chatlog.read().decode()
    except IOError:
        return 'ei voi lukea chatlogia'

    counter = dict()

    if cmd['body'].split()[0] == '!wc':
        if pattern == '':
            pattern = '^.*?$'
        else:
            pattern = re.escape(pattern)

    pattern = re.compile(pattern)

    for row in chatlog.splitlines():
        if re.search('!e?wc', row):
            continue

        row = row.split(maxsplit=3)
        nick = row[2].split('/')[1]
        msg = row[3]

        matches = pattern.findall(msg)

        if matches:
            if counter.get(nick):
                counter[nick] += len(matches)
            else:
                counter[nick] = len(matches)

    return ', '.join('{}: {}'.format(*p) for p in sorted(counter.items(), key=lambda x: x[1], reverse=True))
