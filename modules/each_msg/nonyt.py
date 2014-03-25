import re

def run(msg):
    msg_args = msg['body'].split()
    for a in msg_args:
        if 'nonyt' in ''.join(msg['body'].lower().split()):
            return 'NO NYT :ghammer:'
        if not re.findall('[a-z]|:', msg['body']) and len(re.findall('[A-Z]', msg['body'])) >= 3:
            return ':kasetti:'
        if a.lower().startswith('gnu') or ':gnu:' in msg['body']:
            return 'hehe gnu gnu'
        if a.lower().startswith('mad') or ':mad:' in msg['body']:
            return ':kasetti:'
        if a.startswith('läski'):
            return ':laihduta:'
        if a.lower().startswith('feel') or a.lower().startswith('tajuu'):
            return 'Yea, feel me. The beat is all in me.'
        # ei spoilata
        if a in \
            {'clegane', 'bran', 'joffrey', 'catelyn', 'tyrell', 'brienne',
            'jeor', 'sansa', 'tywin', 'tarly', 'jon', 'wright', 'sandor',
            'waldau', 'arya', 'samwell', 'daenerys', 'melisandre', 'olenna',
            'shae', 'gendry', 'jorah', 'margaery', 'seaworth', 'bolton',
            'mormont', 'tyrion', 'petyr', 'tormund', 'stannis', 'viserys',
            'ygritte', 'tarth', 'robb', 'cersei', 'lannister', 'eddard',
            'ramsay', 'snow', 'greyjoy', 'davos', 'theon', 'baratheon',
            'roose', 'targaryen', 'bronn', 'drogo', 'stark', 'varys',
            'baelish', 'jaime', 'khal', 'robert', 'talisa', 'thrones'}:
            return 30*'EI SPOILATA :kasetti:\n' + msg['mucnick'] + ' perkele'
