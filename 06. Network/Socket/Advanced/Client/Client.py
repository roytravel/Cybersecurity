#-*- coding:utf8 -*-
import socket
import argparse
import socketserver
import os
import datetime

# 파일 데이터와, 크기를 반환
def get_file_data(fullpath):
	with open(fullpath, mode='rb') as f:
		data = f.read()
		size = os.path.getsize(fullpath)
	return data, size

# 데이터 전송 및 수신 결과 반환
def send_and_recv(s, msg):
	s.send(msg.encode())
	result = s.recv(1024)
	return result
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Clinet.py -H [HOST IP] -P [HOST PORT]')
	parser.add_argument('-H', dest='host', help='HOST IP', required=True)
	parser.add_argument('-P', dest='port', help='HOST PORT', required=True)
	parser.add_argument('-T', dest='time', help='IDS TIME', required=True)
	args = parser.parse_args()

	data_transferred = 0

	HOST = args.host
	PORT = args.port
	TIME = args.time

	ADDR = (HOST, int(PORT))
	print ('[+] Connected : {} '.format(ADDR))

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(ADDR)

	path1 = "./ids/test.txt"

	data, size = get_file_data(path1)
	hostname = socket.gethostname()
	information = [hostname, TIME, 'test.txt', str(size)]
	for idx in information:
		result = send_and_recv(s, idx)
		print (result)

	with open(path1, 'rb') as f:
		try:
			data = f.read()
			while data:
				data_transferred = data_transferred + s.send(data)
				data = f.read()
		except Exception as e:
			print (e)
			pass
		# print ("[+] File save completed : {} bytes".format(data_transferred))
	s.close()