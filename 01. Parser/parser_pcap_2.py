# -*- coding:utf8 -*-
import  dpkt
import socket
import urllib


f=open('test.pcap','rb')
pcap=dpkt.pcap.Reader(f)

for timestamp,buf in pcap:
	try:
		eth=dpkt.ethernet.Ethernet(buf)
		ip=eth.data
		tcp=ip.data
		http_req=dpkt.http.Request(tcp.data)
		if http_req.uri.find('search.naver') >= 0:
			print urllib.unquote(http_req.uri)
		elif http_req.uri.find('asp;')>=0:
			print http_req.uri
		elif http_req.method != 'GET' and  http_req.method != 'POST':
			print http_req.method
		if http_req.uri.find('search.naver') >= 0:
			print urllib.unquote(http_req.uri)
		if http_req.uri.method == 'POST' and http_req.uri.find('php') >=0:
			print http_req.body
		# print socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst), http_req.method, http_req.uri
	except:
		pass
f.close()