import urllib.request
import json
import os

triggers = ['!git']


def run(msg):
    # Nyt haetaan se githomo :amd:
    try:
        password = os.environ['githomo']
    except KeyError:
        quit('githomo environment variable not specified KUULIKKO')

    # WTF
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    topUrl = 'http://gitify.fisle.eu/get'
    password_mgr.add_password(None, topUrl, 'dflies', password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    # /WTF
    data = opener.open(topUrl).read().decode()
    commits = json.loads(data)
    results = []
    # vitun dict :kasetti:
    for key, value in commits.items():
        # Enumerate homoilut koska halutaan laittaa \n
        # kaikkiin muihin paitsi vikaan :agree:
        for i, commit in enumerate(value):
            results.append("{} committed into '{}' at {}:\n'{}' {}".format(
                commit['author'],
                commit['name'],
                commit['gitstamp'],
                commit['message'],
                commit['url']))
            # ollaanko vielä lopussa? :o
            if i != len(value) - 1:
                results.append("\n")
    results = ''.join(results)

    return results
