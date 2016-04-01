import os
import random
import re
from time import time

triggers = ['!roll']

def _int(i):
    try: return int(i.replace(' ', ''))
    except: return None

def run(msg):
    msg_args = msg['body'].split(maxsplit=1)
    times, sides, add = re.search('(\d+)?d(\d+)\s*([+-]\s*\d+)?', msg_args[1]).groups()
    times = _int(times) or 1
    sides = int(sides)
    add = _int(add) or 0
    rolls = []
    start = time()
    for t in range(times):
        if time() - start > 5:
            return 'timeout'
        roll = random.randint(1, sides)
        rolls.append(roll)
    total = sum(rolls + [add])
    output = list(map(str, rolls))
    if add != 0:
        output.append('({})'.format(add))
    return '{} = {}'.format(' + '.join(output), total)
