from twython import Twython
from twitterconfig import config

triggers = ['!twitter', '!tweet']

twitter = Twython(config['consumer_key'], 
                    config['consumer_secret'],
                    config['access_token'],
                    config['access_token_secret'])

def run(msg):
    message = msg['body']
    twitter.update_status(status=message)
