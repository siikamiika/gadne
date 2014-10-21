from urllib.request import urlopen

triggers = ['!fisle']


def run(msg):
    return urlopen('http://afk.fisle.eu/gadne').read().decode()
