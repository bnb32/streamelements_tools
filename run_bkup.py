import processing as proc
import sys
import info
import os
import time

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

try:

    if switch=="song":
        song=proc.CurrentSong(channel_id,headers)
        msg="Current song: %s"%song
    
    if switch=="addsong":
        if len(sys.argv)!=5 or proc.Letters(sys.argv[2])=='':
            msg="Error adding song to queue. Please submit a valid song"
        else:
            msg=proc.addSong(sys.argv[2],sys.argv[3],int(sys.argv[4]))
    if switch=="wrongsong":
        if len(sys.argv)!=3:
            msg="Error removing song from queue"
        else:
            msg=proc.wrongSong(sys.argv[2])
    
    if switch=="queue" or switch=="songlist":
        sq=proc.SongQueue()
        msg="Queue: %s"%sq.songlist(sq.ids)
    
    print(msg)
    toc=time.time()
    os.system(cmd%(toc-tic,msg,logname))	
except:
    toc=time.time()
    os.system(cmd%(toc-tic,"Error. Please let DrChessgremlin know you received this message.",logname))
