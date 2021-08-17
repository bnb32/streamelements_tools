import re
import urllib,urllib2
import json
import info
import os
import ast
import time
#from __future__ import division



class SongQueue:
    def __init__(self):
        self.queue={}
        self.channel_id=info.liz_id
        self.token=info.liz_token
        self.qname='queue.json'
        self.fpath=info.directory+'/queue/'
        self.fname=self.fpath+self.qname
        self.lname=time.strftime("%b-%d-%Y")
        self.lcmd='echo """%s""" >> {dir}/logs/{lname}_log.txt'.format(dir=info.directory,lname=self.lname)
        self.qcmd='echo """%s""" > {fname}'.format(fname=self.fname)
        self.headers={'Authorization': "Bearer %s"%(self.token),'accept': 'application/json'}
        
        try: 
            self.readfile()
        except:
            pass
        
        self.ids=self.songids()
        self.checksongs(self.ids)

    def addsong(self,user,title,videoId,_id,length):
        entry={'title':title,'videoId':videoId,'_id':_id,'time':time.time(),'length':length}
        if user in self.queue:
            self.queue[user].append(entry)
        else:
            self.queue[user]=[entry]
        self.writefile()
        return self

    def wrongsong(self,user):
        if user in self.queue:
            self.queue[user].pop(-1)
            self.delCheckUser(user)
            self.writefile()
        return self

    def numsongs(self,user):
        if user in self.queue:
	          return len(self.queue[user])
        else:
	          return 0

    def delCheckUser(self,user): 
        if len(self.queue[user])==0:
            self.queue.pop(user,None)
        return self    
    
    def checksongs(self,songids):
        for user,songs in self.queue.items():
            tmp=[]
            for n,song in enumerate(songs):
                if song['_id'] in songids:
                    tmp.append(song)
            self.queue[user]=tmp	    
            self.delCheckUser(user)
        self.writefile()
        return self

    def infofromid(self,_id):
        val={}
        for user,songs in self.queue.items():
            for s in songs:
                if s['_id']==_id:
                    val['title']=s['title']
                    val['length']=s['length']
                    val['user']=user
        return val    
    
    def gettimes(self,songids):
        lens=[self.infofromid(_id)['length'] for _id in songids]
        return ["%sm %ss"%(divmod(0+sum(lens[0:n]),60)) for n,t in enumerate(lens)]
    
    def songlist(self,songids):
        times=self.gettimes(songids)
        songs={}
        for n,_id in enumerate(songids):
            out=self.infofromid(_id)
            val=[out['title'],out['user'],times[n]]
            songs[n+1]=val
        return songs

    def songids(self):
        r=self.queueinfo()
        return [s['_id'] for s in r]	

    def writefile(self):
        try:
            os.system(self.qcmd%(self.queue))
            os.system(self.lcmd%(self.queue))
        except:
            print("Error writing %s"%(self.qname))

    def readfile(self):
        f=open(self.fname)
        s=f.readline()
        self.queue=ast.literal_eval(s)
        return self

    def queueinfo(self):    
        url = "%s/%s/queue/public"%(info.sr_url,self.channel_id)
        r=self.getr(url,self.headers)
        return r    

    def getr(self,url,heads):
        r = urllib2.Request(url,headers=heads)
        r = urllib2.urlopen(r)
        return json.load(r)
    
def delChars(title):
    return str(re.sub('[^A-Za-z0-9_?#!@/\-()| ]+','',title))

def Letters(line):
    return str(re.sub('[^A-Za-z]+','',line))

def Title(r):
    if r==None:
        return 'None'
    else:	
        return delChars(r['title'])

def Songs(r):    
    songs=['%s. %s '%(n,Title(s)) for n,s in enumerate(r)]
    if len(songs)>0:
        return songs
    else:
        return('Song queue is empty')

def getRequest(url,heads):
    r = urllib2.Request(url,headers=heads)
    r = urllib2.urlopen(r)
    return json.load(r)

def CurrentSong(channel_id,heads):
    url = "%s/%s/playing"%(info.sr_url,channel_id)
    r=getRequest(url,heads)
    return Title(r)

def Settings(channel_id,heads):
    
    url = "%s/%s/settings"%(info.sr_url,channel_id)
    r=getRequest(url,heads)
    settings={}
    settings['max_songs']=r['limits']['users']['free']
    sl=str(r['youtube']['securityLevel'])
    settings['min_views']=info.view_levels[sl]
    settings['min_ratio']=info.ratio_levels[sl]
    settings['max_len']=r['limits']['maxFreeDuration']
    url = "%s/bot/modules/%s"%(info.base_url,channel_id)
    r=getRequest(url,heads)
    settings['min_level']=r['songrequest']['minUserLevel']
    return settings

def SongStats(vid_id,heads):
    url="%s/youtube?videoId=%s"%(info.sr_url,vid_id)
    r=getRequest(url,heads)
    stats={}
    stats['views']=r['statistics']['viewCount']
    stats['likes']=r['statistics']['likeCount']
    stats['dislikes']=r['statistics']['dislikeCount']
    total=stats['likes']+stats['dislikes']
    stats['ratio']=stats['likes']/float(total)
    stats['length']=r['duration']
    return stats

def checkValidVid(channel_id,settings,stats):
    msg=""
    valid=True
    if stats['views']<settings['min_views']:
        msg+="Video must have at least %s views. "%(settings['min_views'])
        valid=False
    if stats['ratio']<settings['min_ratio']:
        msg+="Video must have favorable rating of at least %s. "%(settings['min_ratio'])
        valid=False
    if  stats['length']>settings['max_len']:
        msg+="Video must be less than %s seconds. "%(settings['max_len'])
        valid=False
    return [valid,msg]

def YTsearch(query):
    if 'lyrics' not in query.lower(): 
        query='%s lyrics'%query
    q='+'.join(query.split())
    url="%s/search?part=snippet&type=video&maxResults=1&key=%s&q=%s"%(info.yt_url,info.yt_key,q)
    heads={"accept":"application/json"}
    r=getRequest(url,heads)
    return r['items'][0]['id']['videoId']

def VidId(s):
    if 'v=' in s:
        vid_id=s.split('v=')[1].split('&')[0]
        return [True,vid_id]
    elif '.be/' in s:	
        vid_id=s.split('.be/')[1].split('&')[0]
        return [True,vid_id]
    else:
        return [False,s]

def wrongSong(user):
       
    sq=SongQueue()
    if user in sq.queue:
        _id=sq.queue[user][-1]['_id']
        title=sq.queue[user][-1]['title']
        sq.wrongsong(user)
    else:
        return("You have no songs in the queue. "+info.beta_msg)

    handler=urllib2.HTTPHandler(debuglevel=1)
    opener=urllib2.build_opener(handler)
    
    url = "%s/%s/queue/%s"%(info.sr_url,sq.channel_id,_id)
    r=urllib2.Request(url,headers=sq.headers)
    r.get_method=lambda:'DELETE'
    
    try:
        conn=opener.open(r)
    except urllib2.HTTPError,e:
        #return("Error opening endpoint")
        conn=e

    if conn.code==201:
        return("Removed from queue: %s"%(title))
    else:
        return("Error connecting to server")

def addSong(vid_id,user,level):    

    sq=SongQueue()
    url = "%s/%s/queue"%(info.sr_url,sq.channel_id)
    
    settings=info.settings
    min_level=int(settings['min_level'])
    
    if min_level>level:
        return("Song request is limited to: %s"%(info.user_levels[min_level]))
    if sq.numsongs(user)>=settings['max_songs']	and level<info.exempt_level:
        return("You cannot have more than %s songs in the queue at a time"%(settings['max_songs']))

    [tmp,vid_id]=VidId(vid_id)
    if tmp:
        try: stats=SongStats(vid_id,sq.headers)
        except:
            return("No matches to that videoId. "+info.beta_msg)
        [valid_vid,msgs]=checkValidVid(sq.channel_id,settings,stats)
    else:	
        try: vid_id=YTsearch(vid_id)
        except:
            return("No matches to that keyword query. "+info.beta_msg)
        stats=SongStats(vid_id,sq.headers)
        [valid_vid,msgs]=checkValidVid(sq.channel_id,settings,stats)
    if not(valid_vid) and level<info.exempt_level:
        return(msgs)
    	
    handler=urllib2.HTTPHandler(debuglevel=1)
    opener=urllib2.build_opener(handler)
    data={'video':vid_id}
    
    r=urllib2.Request(url,data=urllib.urlencode(data),headers=sq.headers)
    r.get_method=lambda:'POST'
    
    try:
        conn=opener.open(r)
    except urllib2.HTTPError,e:
        #return("Error opening endpoint")
        conn=e
    
    if conn.code==200:
        out=conn.read()
        out=json.loads(out)
        song=Title(out)
        sq.addsong(user,song,out['videoId'],out['_id'],out['duration'])
        return("Added to queue: %s"%song)
    else:
        return("Error connecting to server. "+info.beta_msg)

   
