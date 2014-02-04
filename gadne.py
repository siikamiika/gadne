import sys
import logging
import getpass
import os
import datetime
import re
from optparse import OptionParser
import sleekxmpp
from concurrent.futures import ThreadPoolExecutor

# how to include triggers in a module:
# triggers = ['!something', '!else']
# also: triggers = {'!smt': 'something'}
module_triggers = dict()
eachmsg_modulelist = []
eachword_modulelist = []

moduledirs = dict(
    (
        folder.split(os.sep)[-1],
        ['.'.join(os.path.join(folder, f[:-3]).split(os.sep))
        for f in files if f[-3:] == '.py' and f != '__init__.py']
    )
    for folder, folders, files in os.walk('modules')
    if '__pycache__' not in folder and 'unused' not in folder
)

for folder, mlist in moduledirs.items():
    for module in mlist:
        exec('import {}'.format(module))
        if folder == 'modules':
            exec('for t in {0}.triggers: module_triggers[t] = {0}'.format(module))
        elif folder == 'each_msg':
            exec('eachmsg_modulelist.append({})'.format(module))
        elif folder == 'each_word':
            exec('eachword_modulelist.append({})'.format(module))

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
            self.send_message(mto=msg['from'].bare, mbody=text,
                mtype='groupchat')

        #def send_back(text):
        #    self.send_message(mto=msg['from'], mbody=text, mtype='chat')

        if len(msg_args) != 0 and msg['mucnick'] != self.nick:
            time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S ')
            open('chatlog.log', 'a').write(
                time+str(msg['from'])+'/'+msg['id']+': '+
                msg['body'].replace('\n', '')+'\n'
            )

            for m in eachmsg_modulelist:
                self.tp.submit(lambda msg=msg: send(m.run(msg)))

            if msg_args[0] in module_triggers:
                self.tp.submit(lambda msg=msg:
                        send(module_triggers[msg_args[0]].run(msg))
                    )

            for w in eachword_modulelist:
                for arg in msg_args:
                    self.tp.submit(lambda arg=arg: send(w.run(arg)))


if __name__ == '__main__':

    optp = OptionParser()

    optp.add_option('-q', '--quiet',
            help='set logging to ERROR',
            action='store_const',
            dest='loglevel',
            const=logging.ERROR,
            default=logging.INFO
        )
    optp.add_option('-d', '--debug',
            help='set logging to DEBUG',
            action='store_const',
            dest='loglevel',
            const=logging.DEBUG,
            default=logging.INFO
        )
    optp.add_option('-v', '--verbose',
            help='set logging to COMM',
            action='store_const',
            dest='loglevel',
            const=5,
            default=logging.INFO
        )

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
