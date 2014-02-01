import sys
import logging
import getpass
import os
import datetime
import re
from optparse import OptionParser

import sleekxmpp
import modules.unica
import modules.sodexo
import modules.turkuweather
import modules.youtube
import modules.bus
import modules.cleverbot
import modules.wc
import modules.pasi
import modules.revimg
import modules.title
import modules.katse
import modules.log
import modules.spam

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
        def send_all(text):
            self.send_message(mto=msg['from'].bare, mbody=text, mtype='groupchat')

        def send_back(text):
            self.send_message(mto=msg['from'], mbody=text, mtype='chat')

        if len(msg_args) != 0 and msg['mucnick'] != self.nick:
            time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S ')
            open('chatlog.log', 'a').write(time+str(msg['from'])+'/'+msg['id']+': '+msg['body'].replace('\n', '')+'\n')
            if msg_args[0] == '!btc':
                send_all(modules.katse.katse('btc'))
            if msg_args[0] == '!ltc':
                send_all(modules.katse.katse('ltc'))
            if msg_args[0] == '!xpm':
                send_all(modules.katse.katse('xpm'))
            if msg_args[0] == '!ict':
                send_all(modules.sodexo.lounas(msg_args[1:]))
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
                send_all(modules.unica.lounas(unica[msg_args[0]], msg_args[1:]))
            if msg_args[0] == '!unica':
                send_all(str(unica))
            if msg_args[0] == '!sää':
                send_all(modules.turkuweather.weather(msg_args[1:]))
            if msg_args[0] == '!bus':
                send_back(modules.bus.aikataulu(msg_args[1:], str(msg['mucnick'])))
            if msg_args[0] == '!wc':
                send_all(modules.wc.count(msg))
            if msg_args[0] == '!spam':
                send_all(modules.spam.spam())
            if msg_args[0] == '!find':
                send_all(modules.log.find(msg))
            if msg_args[0] == '!pasi':
                send_all('!perjantai')
            if msg['body'] == 'Kyllä, nyt on perjantai' and str(msg['mucnick']) == 'Doodlebot':
                send_all(modules.pasi.radio())
            if msg_args[0] == 'gadne:':
                kysymys = msg['body'].lstrip('gadne: ')
                vastaus = modules.cleverbot.Cleverbot().ask(kysymys)
                send_all(vastaus)
            if 'nonyt' in ''.join(msg['body'].lower().split()):
                send_all('NO NYT :ghammer:')

            for a in msg_args:
                if a is not None:
                    ytinfo = modules.youtube.info(a)
                    if ytinfo != '':
                        send_all(ytinfo)
                    else:
                        send_all(modules.title.get(a))
                if re.match('https?://.*?\.(gif|png|jpe?g).*', a):
                    send_all(modules.revimg.desc(a))

            for a in msg_args:
                if not re.findall('[a-z]|:', msg['body']) and len(re.findall('[A-Z]', msg['body'])) >= 3:
                    send_all(':kasetti:')
                    break
                if a.lower().startswith('gnu') or a == ':gnu:':
                    send_all('hehe gnu gnu')
                    break
                if a.lower().startswith('mad') or a == ':mad:':
                    send_all(':kasetti:')
                    break
                if a.startswith('läski'):
                    send_all(':laihduta:')
                    break
                if a.lower().startswith('feel') or a.lower().startswith('tajuu'):
                    send_all('Yea, feel me. The beat is all in me.')
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
