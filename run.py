import processing as proc
import sys
import info
import os
import time
import urllib2

if len(sys.argv)<2:
    print("Specify a valid function")
    exit()

switch=sys.argv[1]
channel_id=info.liz_id
headers = {'accept': 'application/json'}
token=info.liz_token


tstring=time.strftime("%b-%d-%Y-%H:%M:%S")
logname=time.strftime("%b-%d-%Y")
tic=time.time()

cmd='echo "%s %s" >> {dir}/logs/%s_log.txt'.format(dir=info.directory)
os.system(cmd%(tstring,sys.argv[1:],logname))

msg=""


base_url="http://drchessgremlin.ddns.net/tools/run.php?script=%s"

try:

    if switch=="song":
	url=base_url%"song"
	msg=urllib2.urlopen(url).read()

    if switch=="addsong":
        if len(sys.argv)!=5 or proc.Letters(sys.argv[2])=='':
            msg="Error adding song to queue. Please submit a valid song"
        else:
            url=base_url%"addsong"+"&song=%s&user=%s&level=%s"%(sys.argv[2],sys.argv[3],sys.argv[4])
            msg=urllib2.urlopen(url).read()
    
    if switch=="wrongsong":
        if len(sys.argv)!=3:
            msg="Error removing song from queue"
        else:
            url=base_url%"wrongsong"+"&user=%s"%(sys.argv[2])
            msg=urllib2.urlopen(url).read()

    if switch=="queue" or switch=="songlist":
	url=base_url%"queue"
	msg=urllib2.urlopen(url).read()
    
    print(msg)
    toc=time.time()
    os.system(cmd%(toc-tic,msg,logname))	
except:
    toc=time.time()
    os.system(cmd%(toc-tic,"Error. Please let DrChessgremlin know you received this message.",logname))
