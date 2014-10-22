import urllib.request
import json
import os

triggers = ['!git']


def run(msg):
    # Nyt haetaan se githomo :amd:
    try:
        password = os.environ['githomo']
    except KeyError:
        return 'githomo environment variable not specified KUULIKKO'

    topUrl = 'http://gitify.fisle.eu/get'
    # Nyt katsetaan se määrä
    count = msg['body'].split()[1]
    if count:
        try:
            topUrl = '{}/{}'.format(topUrl, int(count))
        except ValueError:
            return 'Olet homo jos luet tämän :cool:'

    # WTF
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, topUrl, 'dflies', password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    # /WTF
    data = opener.open(topUrl).read().decode()
    commits = json.loads(data)['commits']
    return '\n'.join(["{} committed into '{}' at {}:\n'{}' {}".format(
        commit['author'],
        commit['name'],
        commit['gitstamp'],
        commit['message'],
        commit['url']) for commit in commits])
