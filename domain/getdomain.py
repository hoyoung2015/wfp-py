# -*- coding: utf-8 -*-
"""
从nutch采集的mongodb库中导出外部链接的域名
"""
import sys
import urllib
import pymongo
import getopt

def usage():
	print '-h host'
	print '-p prot'
	print '-d domain'
	print '-o output'
if len(sys.argv)==1:
	usage()
	sys.exit()

opts, args = getopt.getopt(sys.argv[1:], "h:p:d:o:")

host = "127.0.0.1"
port = "27017"
output = ""
domain = ""
for op, value in opts:
    if op == "-h":
        host = value
    elif op == "-p":
        port = value
    elif op == "-d":
        domain = value
    elif op == "-o":
        output = value
#print host
#print port
#print output
#print domain

reload(sys)
sys.setdefaultencoding('utf-8')

client = pymongo.MongoClient(host, int(port))
db = client.nutch

extlinks = set()
for item in db.df_webpage.find():
    if item.has_key('extlinks'):
        for (k,v) in item['extlinks'].items():
            extlinks.add(k)

indomains = set()           
outdomains = set()           
#domain = 'dfpv.com.cn'            
for url in extlinks:
    #print url
    proto, rest=urllib.splittype(url)
    res, rest = urllib.splithost(rest) 
    res = res.replace('·','.')
    #print res
    if domain in res:
        indomains.add(res)
    else:
        outdomains.add(res)
if len(outdomains)==0:
    print 'There is no outdomains.'
    sys.exit()
f = file(output,'w+')
for d in outdomains:
    f.write(d+'\n')
f.close()
print 'urls:',len(outdomains)
print 'output:',output
print 'successful'
        
        



    
