#-*- coding:utf8 -*-
from socket import *

HOST='' #공백 (없어도됨)
PORT=31337 #포트번호 할당
ADDR=(HOST,PORT)    #주소를 튜플로
s=socket(AF_INET,SOCK_STREAM)   #전화기사고
s.bind(ADDR)    #전화번호받고
s.listen(1)#클라이언트 두명만 가능
while True:
	conn, addr=s.accept()   #연결이오면
	print 'connected from',addr #번호알려주고
	while True:
		data=conn.recv(1024)    #1024바이트만큼받고
		if not data:
			break
		elif data=="V3G4":
			conn.send('Key is FuCk_YoU_BaBy')
		else:
			conn.send('your data is %s'% data)  #%s만큼 받았다고 알려주고
	conn.close()    #연결종료
s.close()#통신끝
