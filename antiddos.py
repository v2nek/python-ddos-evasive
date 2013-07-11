#!/usr/bin/python2.7
# coding: utf-8

#: Title	:Python DDoS evasive script
#: Date		:2013-07-11
#: Author	:Ivan Borovkov <v2nek.sev@gmail.com>
#: Version	:0.4
#: Description	:Find out flooding IP addresses and block them with ipset.

import time
import sys
import hashlib
import redis
import os
from subprocess import Popen, PIPE, call


# here is whitelist of allowed IP's 2
white = ['127.0.0.1']
# here is list of allowed file extensions
wextens = ['.jpg','.css','.js','.jpeg','.ico','.png','.gif','7z','tar','gz','zip','.swf']

# time to expire of record
expiretime = 10
reqlimit = 10

whitestatuses = ['206']

logpath = '/var/log/nginx/'


tm = 0



while 1:
	try:
		line = sys.stdin.readline()
	except KeyboardInterrupt:
		break
	if not line:
		break
	try:
		r.keys('%s:global_site_req' % site)
	except:
		r = redis.Redis(host='localhost', port=6379, db=0)
	if len(r.keys('%s:global_site_req' % site)) > 0:
		num = int(r.get('%s:global_site_req' % site))
		r.set('%s:global_site_req' % site, num)
	else:
		r.set('%s:global_site_req' % site, 1)
	
	if ( (int(time.time()) - tm) > 300 ):
		if ( int(os.stat(logpath + 'all.log').st_size) > 500000000 ): pid = Popen(["/root/unddos-monitors/clearlog.sh",site], stdout=PIPE).pid
		tm = int(time.time())

	ln = line.split('|+|')

	if ( len(ln) < 8 ): continue

	if ( int(ln[3]) != 400 ):
		try:
			keysource = str(ln[0]) + "|" + str(ln[2].split(' ')[1]) + "|" + str(ln[1])
		except:
			continue
	else: 
		call(["/root/python-ddos-evasive/ban.sh", str(ln[1]), str(ln[0])])
		continue

	if ( int(ln[3]) == 444 ):
		try:
			call(["/root/python-ddos-evasive/ban.sh", str(ln[1]), str(ln[0])])
		except:
			print "failed to ban"
			continue
		continue

	if white.count( str(ln[1]) ) > 0:
		continue

	if whitestatuses.count( str(ln[3]) ) > 0:
		continue

	ignoreme = 0
	for elem in wextens:
		if elem in str(ln[2].split(' ')[1]):
			ignoreme = 1
			break
	if ignoreme > 0: continue


	site_id = int(r.get('%s:global_site_req' % site))

	key = hashlib.md5(keysource).hexdigest()
	r.set( '%s:%s:%s' % (site, str(key), str(site_id)), keysource )
	r.expire( '%s:%s:%s' % (site, str(key), str(site_id)), expiretime)
	r.incr('%s:global_site_req' % site)
	mas = r.keys('%s:%s:*' % (site, str(key)))
	if len(mas) > reqlimit:
		try:
			call(["/root/python-ddos-evasive/ban.sh", str(ln[1]), str(ln[0]), "key"])
		except:
			continue
