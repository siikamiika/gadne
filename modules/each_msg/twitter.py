from twython import Twython
import re
from twitterconfig import config


twitter = Twython(config['consumer_key'], 
                    config['consumer_secret'],
                    config['access_token'],
                    config['access_token_secret'])

def run(msg):
    regexp = re.compile(r'(^|\s)#[^\s]+')
    message = msg['body']
    if regexp.search(message):
        twitter.update_status(status = message)
