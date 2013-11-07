import re
from collections import Counter

def count(msg):
	try:
		with open('chatlog.log', 'rb') as chatlog:
			try:
				chatlog = chatlog.read().decode()
				viesti = msg['body'].lstrip('!wc ')
			except UnicodeDecodeError:
				chatlog = chatlog.read().decode('latin-1')
				viesti = msg['body'].encode("latin-1").decode("latin-1").lstrip('!wc ')
	except IOError:
		return 'ei voi lukea chatlogia'
	nimet = re.findall('(?:'+msg['from'].bare+'/)(.*?)(?:/.*?:\s)(?:.*?)(?:'+re.escape(viesti)+')', chatlog)
	wc = Counter(nimet)
	return str(wc).lstrip('Counter')
