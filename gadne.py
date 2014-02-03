import sys
import logging
import getpass
import os
import datetime
import re
from optparse import OptionParser
from concurrent.futures import ThreadPoolExecutor

import sleekxmpp

modules = [
    f[:-3] for f in os.listdir('modules')
    if os.path.isfile('modules/'+f) and f != '__init__.py' and f[-3:] == '.py'
]

each_msg = [
    f[:-3] for f in os.listdir('modules/each_msg')
    if os.path.isfile('modules/each_msg/'+f) and f != '__init__.py' and f[-3:] == '.py'
]

each_word = [
    f[:-3] for f in os.listdir('modules/each_word')
    if os.path.isfile('modules/each_word/'+f) and f != '__init__.py' and f[-3:] == '.py'
]

module_triggers = dict()
eachmsg_modulelist = []
eachword_modulelist = []


for module in modules:
    exec('import modules.'+module)
    exec('from modules.'+module+' import triggers as '+module+'_triggers')
    exec('for t in '+module+'_triggers: module_triggers[t] = modules.'+module)

for module in each_msg:
    exec('import modules.each_msg.'+module)
    exec('eachmsg_modulelist.append(modules.each_msg.'+module+')')

for module in each_word:
    exec('import modules.each_word.'+module)
    exec('eachword_modulelist.append(modules.each_word.'+module+')')

class MUCBot(sleekxmpp.ClientXMPP):

    tp = ThreadPoolExecutor(max_workers=5)

    def __init__(self, jid, password, room, nick):

        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)

    def start(self, event):

        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)

    def muc_message(self, msg):

        msg_args = msg['body'].split()

        def send(text):
            self.send_message(mto=msg['from'].bare, mbody=text, mtype='groupchat')

        def send_back(text):
            self.send_message(mto=msg['from'], mbody=text, mtype='chat')


        if len(msg_args) != 0 and msg['mucnick'] != self.nick:
            time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S ')
            open('chatlog.log', 'a').write(time+str(msg['from'])+'/'+msg['id']+': '+msg['body'].replace('\n', '')+'\n')

            for m in eachmsg_modulelist:
                self.tp.submit(lambda msg=msg: send(m.run(msg)))

            if msg_args[0] in module_triggers:
                self.tp.submit(lambda msg=msg: send(module_triggers[msg_args[0]].run(msg)))

            for w in eachword_modulelist:
                for arg in msg_args:
                    self.tp.submit(lambda arg=arg: send(w.run(arg)))
                

if __name__ == '__main__':

    optp = OptionParser()

    optp.add_option('-q', '--quiet', help='set logging to ERROR', action='store_const', dest='loglevel', const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM', action='store_const', dest='loglevel', const=5, default=logging.INFO)

    optp.add_option("-j", "--jid", dest="jid", help="JID to use")
    optp.add_option("-p", "--password", dest="password", help="password to use")
    optp.add_option("-r", "--room", dest="room", help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick", help="MUC nickname")

    opts, args = optp.parse_args()

    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = input("MUC room: ")
    if opts.nick is None:
        opts.nick = input("MUC nickname: ")

    xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
