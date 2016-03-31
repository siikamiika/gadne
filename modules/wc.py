import re

triggers = ['!wc', '!ewc']
HELP = \
"""!wc <word or words>, !ewc <pattern>
!wc: how many times <word or words> has been mentioned (whitespace delimited; doesn't count "examplee" as "example")
!ewc: regex enabled"""

def run(cmd):

    pattern = cmd['body'].split(None, 1)
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

    re_options = 0

    count_commands = False

    if pattern.startswith('!'):
        pattern = r'^' + re.escape(pattern) + r'.*'
        count_commands = True
    elif cmd['body'].split()[0] == '!wc':
        if pattern == '':
            pattern = r'^.*?$'
        else:
            pattern = r'(?:^|(?<=\s)){}(?:$|(?=\s))'.format(re.escape(pattern))
            re_options |= re.IGNORECASE

    pattern = re.compile(pattern, re_options)

    for row in chatlog.splitlines():

        row = row.split(None, 3) + ['']
        nick = row[2].split('/')[1]
        msg = row[3]

        if not count_commands and re.match('!.*', msg):
            continue

        matches = pattern.findall(msg)

        if matches:
            if counter.get(nick):
                counter[nick] += len(matches)
            else:
                counter[nick] = len(matches)

    return ', '.join('{}: {}'.format(*p) for p in sorted(counter.items(), key=lambda x: x[1], reverse=True))
