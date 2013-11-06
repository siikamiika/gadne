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

		if len(msg_args) != 0 and msg['mucnick'] != self.nick:
			time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S ')
			open('chatlog.log', 'a').write(time+str(msg['from'])+'/'+msg['id']+': '+msg['body'].replace('\n', '')+'\n')
			viesti = ''
			if msg_args[0] == '!assari':
				viesti = modules.unica.lounas('assarin-ullakko/', msg_args[1:])
			if msg_args[0] == '!ict':
				viesti = modules.sodexo.lounas(msg_args[1:])
			if msg_args[0] == '!tottis':
				viesti = modules.unica.lounas('tottisalmi/', msg_args[1:])
			if msg_args[0] == '!delica':
				viesti = modules.unica.lounas('delica/', msg_args[1:])
			if msg_args[0] == '!sää':
				viesti = modules.turkuweather.weather(msg_args[1:])
			if msg_args[0] == '!bus':
				self.send_message(mto=msg['from'], mbody=modules.bus.aikataulu(msg_args[1:], str(msg['mucnick'])), mtype='chat')
			if msg_args[0] == '!wc':
				self.send_message(mto=msg['from'].bare, mbody=modules.wc.count(' '.join(msg_args[1:])), mtype='groupchat')
			if msg_args[0] == 'gadne:':
				kysymys = msg['body'].lstrip('gadne: ')
				vastaus = modules.cleverbot.Cleverbot().ask(kysymys)
				self.send_message(mto=msg['from'].bare, mbody=vastaus, mtype='groupchat')
			if 'nonyt' in ''.join(msg['body'].lower().split()):
				self.send_message(mto=msg['from'].bare, mbody='NO NYT :ghammer:', mtype='groupchat')

			for a in msg_args:
				if a is not None:
					ytinfo = modules.youtube.info(a)
					if ytinfo != '':
						self.send_message(mto=msg['from'].bare, mbody=ytinfo, mtype='groupchat')
				if a.lower().startswith('gnu') or a == ':gnu:':
					viesti = 'hehe gnu gnu'
				if a.lower().startswith('mad') or a == ':mad:':
                                        viesti = ':kasetti:'
				if a.startswith('läski'):
					viesti = ':laihduta:'

			if viesti != '':
				self.send_message(mto=msg['from'].bare, mbody=viesti, mtype='groupchat')
				

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
