import random

triggers = ['!spam']

def run(lol):
    ruokalista = ['Egg', 'Bacon', 'Sausage']
    random.shuffle(ruokalista)
    tilaus = []

    for _ in range(random.randint(1, 7)):
        valinta = random.randrange(2)
        if valinta and len(ruokalista):
            ruoka = ruokalista.pop()
        else:
            ruoka = 'Spam'
        tilaus.append(ruoka)
        
    return ', '.join(tilaus)+' and Spam'
