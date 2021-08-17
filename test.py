import processing as proc
import info
import os
import subprocess
import json
import ast
import urllib2

url="http://drchessgremlin.ddns.net/tools/run.php?script=song"
#heads={'accept':'application/json'}
#r = urllib2.Request(url,headers=heads)
r = urllib2.urlopen(url)
print(r.read())
