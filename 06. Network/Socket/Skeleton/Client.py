#-*- coding:utf8 -*-
from socket import *

HOST='127.0.0.1'
PORT=31337
ADDR=(HOST,PORT)
s=socket(AF_INET,SOCK_STREAM)
s.connect(ADDR)
while True:
	for i in range(ord('A'),ord('Z')+1):
		for j in range(0,10):
			for k in range(ord('A'), ord('Z') + 1):
				for l in range(0,10):
					data=chr(i)+str(j)+chr(k)+str(l)
					s.send(data) #데이터 있으면 보내고
					data=s.recv(1024)#서버에서 주는 응답 1024크기받고
					if not data:#서버에서 암것도 안주면
						break #빠이
					elif data.find('Key')==0: #find의 return value = index
						print data
	break
	s.close() #빠이
