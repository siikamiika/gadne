import os
import random
import re

triggers = ['!roll']

def _int(i):
    try: return int(i)
    except: return None

def run(msg):
    msg_args = msg['body'].split()
    times, sides, add = re.search('(\d+)?d(\d+)([+-]\d+)?', msg_args[1]).groups()
    times = _int(times) or 1
    sides = int(sides)
    add = _int(add) or 0
    output = []
    for t in range(times):
        output.append(str(random.randint(1, sides) + add))
    return ', '.join(output)

