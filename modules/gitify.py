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

    # WTF
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    topUrl = 'http://gitify.fisle.eu/get'
    password_mgr.add_password(None, topUrl, 'dflies', password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    # /WTF
    data = opener.open(topUrl).read().decode()
    commits = json.loads(data)['commits']
    return  '\n'.join(["{} committed into '{}' at {}:\n'{}' {}".format(
            commit['author'],
            commit['name'],
            commit['gitstamp'],
            commit['message'],
            commit['url']) for commit in commits])
