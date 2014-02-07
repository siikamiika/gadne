import sys
import logging
import getpass
import os
import datetime
import re
from optparse import OptionParser
import sleekxmpp
from threading import Thread

moduledirs = dict(
    (
        folder.split(os.sep)[-1],
        ['.'.join(os.path.join(folder, f[:-3]).split(os.sep))
        for f in files if f[-3:] == '.py' and f != '__init__.py']
    )
    for folder, folders, files in os.walk('modules')
    if '__pycache__' not in folder and 'unused' not in folder
)

for ml in moduledirs.values():
    for m in ml: exec('import '+m)

m_container = dict(
    (md, [eval(m) for m in ml])
    for md, ml in moduledirs.items()
)

class MUCBot(sleekxmpp.ClientXMPP):

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

        def send(module, text):
            self.send_message(mto=msg['from'].bare, mbody=module.run(text),
                    mtype='groupchat')

        if len(msg_args) != 0 and msg['mucnick'] != self.nick:
            with open('chatlog.log', 'a') as log:
                log.write('{0} {1}/{2}: {3}\n'.format(
                    datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                    msg['from'], msg['id'], msg['body'].replace('\n', '')
                    )
                )

            for m in m_container['each_msg']:
                Thread(target=send, args=(m, msg)).start()

            for m in m_container['modules']:
                if msg_args[0] in m.triggers:
                    Thread(target=send, args=(m, msg)).start()

            for m in m_container['each_word']:
                for arg in msg_args:
                    Thread(target=send, args=(m, arg)).start()

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
