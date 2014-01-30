import random

def spam():
    ruokalista = ['Egg', 'Bacon', 'Sausage', 'Spam', 'Spam']
    tilaus = []
    tmp = None

    for _ in range(random.randint(5, 10)):
        ruoka = random.choice(ruokalista)
        if ruoka is 'Spam' or ruoka is not tmp:
            tilaus.append(ruoka)
            tmp = ruoka

    return ', '.join(tilaus)+' and Spam'
