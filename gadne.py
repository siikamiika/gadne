import sys
import logging
import getpass
import os
import datetime
import re
from optparse import OptionParser
from concurrent.futures import ThreadPoolExecutor

import sleekxmpp
import modules.unica
import modules.sodexo
import modules.turkuweather
import modules.bus
import modules.cleverbot
import modules.wc
import modules.pasi
import modules.katse
import modules.log
import modules.spam
import modules.link

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
            if msg_args[0] == '!btc':
                self.tp.submit(lambda txt: send(modules.katse.katse(txt)), 'btc')
            if msg_args[0] == '!ltc':
                self.tp.submit(lambda txt: send(modules.katse.katse(txt)), 'ltc')
            if msg_args[0] == '!xpm':
                self.tp.submit(lambda txt: send(modules.katse.katse(txt)), 'xpm')
            if msg_args[0] == '!ict':
                self.tp.submit(lambda txt: send(modules.sodexo.lounas(txt)), msg_args[1:])
            unica = {
                '!assari': 'assarin-ullakko/',
                '!tottis': 'tottisalmi/',
                '!delica': 'delica/',
                '!brygge': 'brygge/',
                '!deli': 'deli-pharma/',
                '!dent': 'dental/',
                '!mac': 'macciavelli/',
                '!mikro': 'mikro/',
                '!nutri': 'nutritio/',
                '!rk': 'ruokakello/'
            }
            if msg_args[0] in unica:
                msg_args[0] = unica[msg_args[0]]
                self.tp.submit(lambda txt: send(modules.unica.lounas(txt)), msg_args)
            if msg_args[0] == '!unica':
                self.tp.submit(lambda txt: send(txt), str(unica))
            if msg_args[0] == '!sää':
                self.tp.submit(lambda txt: send(modules.turkuweather.weather(txt)), msg_args[1:])
            if msg_args[0] == '!bus':
                self.tp.submit(lambda txt: send_back(modules.bus.aikataulu(txt)), msg)
            if msg_args[0] == '!wc':
                self.tp.submit(lambda txt: send(modules.wc.count(txt)), msg)
            if msg_args[0] == '!spam':
                self.tp.submit(lambda txt: send(modules.spam.spam(txt)), 'juuh elikkäs') # lambda vaatii
            if msg_args[0] == '!find':
                self.tp.submit(lambda txt: send(modules.log.find(txt)), msg)
            if msg_args[0] == '!pasi':
                self.tp.submit(lambda txt: send(txt), '!perjantai')
            if msg['body'] == 'Kyllä, nyt on perjantai' and str(msg['mucnick']) == 'Doodlebot':
                self.tp.submit(lambda txt: send(modules.pasi.radio()))
            if msg_args[0] == 'gadne:':
                kysymys = msg['body'].lstrip('gadne: ')
                self.tp.submit(lambda txt: send(modules.cleverbot.Cleverbot().ask(txt)), kysymys)
            if 'nonyt' in ''.join(msg['body'].lower().split()):
                self.tp.submit(lambda txt: send(txt), 'NO NYT :ghammer:')

            for maybe_url in msg_args:
                # youtube info, title, reverse image search
                self.tp.submit(lambda txt: send(modules.link.desc(txt)), maybe_url)

            for a in msg_args:
                if not re.findall('[a-z]|:', msg['body']) and len(re.findall('[A-Z]', msg['body'])) >= 3:
                    self.tp.submit(lambda txt: send(txt), ':kasetti:')
                    break
                if a.lower().startswith('gnu') or a == ':gnu:':
                    self.tp.submit(lambda txt: send(txt), 'hehe gnu gnu')
                    break
                if a.lower().startswith('mad') or a == ':mad:':
                    self.tp.submit(lambda txt: send(txt), ':kasetti:')
                    break
                if a.startswith('läski'):
                    self.tp.submit(lambda txt: send(txt), ':laihduta:')
                    break
                if a.lower().startswith('feel') or a.lower().startswith('tajuu'):
                    self.tp.submit(lambda txt: send(txt), 'Yea, feel me. The beat is all in me.')
                    break
                # [20:11:58] <johan> NYT VITTUUN TOI
                # [20:15:59] <edgar> vittu mä repeen tääl :D:D:D
                # [20:19:16] <edgar> kiitos johanille päivän nauruist :D
                #if a.lower().startswith('win'):
                #   viesti = 'Juuh elikkäs joku Windows :grage:'
                

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
