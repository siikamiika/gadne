# idea:
# https://codegolf.stackexchange.com/questions/123685/covfefify-a-string
# (modified)
triggers = ['!covfefe']

VOWELS = 'aeiouyäö'
TOGGLE_VOICED = {
    # unvoiced --> voiced
    'c': 'g',
    'f': 'v',
    'k': 'g',
    'p': 'b',
    's': 'z',
    't': 'd',
    # voiced --> unvoiced
    'g': 'k',
    'v': 'f',
    'b': 'p',
    'z': 's',
    'd': 't',
}

def covfefe(word):
    output = []

    first_vowel = None
    last_consonant = None
    previous_vowel = None
    repeat_vowel = None
    stop = False

    for c in word:
        if not stop:
            output.append(c)

        if c.lower() in VOWELS:
            previous_vowel = c
            if not first_vowel:
                first_vowel = c
            elif last_consonant:
                repeat_vowel = c
                break
        else:
            if first_vowel and not last_consonant:
                last_consonant = c
                stop = True

    if not last_consonant:
        return word

    repeat_consonant = TOGGLE_VOICED.get(last_consonant.lower()) or last_consonant
    if last_consonant.isupper():
        repeat_consonant = repeat_consonant.upper()
    output.append((repeat_consonant + (repeat_vowel or previous_vowel))*2)

    return ''.join(output)

def run(msg):
    msg_args = msg['body'].split()
    return ' '.join(map(covfefe, msg_args[1:]))
