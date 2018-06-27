# coding:utf-8
from scapy.all import *
import re
from operator import itemgetter

# pcap ファイルの読み込み
packets = rdpcap('hidden.pcap').filter(lambda p: Raw in p and TCP in p and p[TCP].sport == 80)
sessions = packets.sessions()
sessions_list = [sessions[s] for s in sessions]

contents = []
d = {}
for session in sessions_list:
	for i, p in enumerate(session): 
		data = p[Raw].load
		if i == 0:
			m = re.search(b'(?P<bytes>(\d+)-(\d+))/(\d+)\r\n\r\n(?P<payload>(.*))', data, flags=(re.MULTILINE | re.DOTALL))
			if m is not None:
				d = m.groupdict()
		else:
			d['payload'] += data
	contents.append(d)

new_contents = sorted(contents, key=itemgetter('bytes'))
f = open('flag.png', 'wb')
for i in new_contents:
	f.write(i['payload']) 
f.close()
