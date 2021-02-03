# -*- coding:utf-8 -*-

import socket, threading
import os
import io


class TCPServerThread(threading.Thread):
    def __init__(self, tcpServerThreads, connections, connection, clientAddress):
        threading.Thread.__init__(self)

        self.tcpServerThreads = tcpServerThreads
        self.connections = connections
        self.connection = connection
        self.clientAddress = clientAddress


    def run(self):
        try:
            # socket 객체 생성
            s = socket.socket()

            data_transferred = 0
            
            # recv는 socket에 메시지가 수신될 때 까지 대기(accept와 동일하게.)
            # 만약 1024보다 수신할 데이터가 크다면 가져오지 못했던 것을 가져옴
            filename = self.connection.recv(1024)
            print ('[+] Received filename : {}'.format(filename.decode('utf-8')))

            # 파일 이름 수신 완료 메시지 전송
            f_msg = "[1] TCP Server : File name [{}] query ok".format(filename.decode('utf-8'))
            self.connection.send(f_msg.encode('utf-8'))

            # 파일 사이즈 수신 완료 메시지 전송
            size = self.connection.recv(1024)
            s_msg = "[2] TCP Server : File size [{}] query ok".format(size.decode('utf-8'))

            # 수신 받은 파일 크기 확인
            print ('[+] Received file size : {} Bytes'.format(size.decode('utf-8')))
            self.connection.send(s_msg.encode('utf-8'))

            # 수신 받을 크기 만큼 data를 읽어서 filename으로 이름을 설정하여 저장
            data = self.connection.recv(1024)
            if not data:
                print("전송 중 오류 발생")
                return

            with open(filename.decode(), 'wb') as f:
                try:
                    while data:
                        f.write(bytes(data))
                        data_transferred = data_transferred + len(data)
                        data = self.connection.recv(1024)
                    print ("[+] Received finished\n")

                    # 파일 수신 및 저장 완료 메시지 전송
                    self.connection.send("[3] TCP Server : File transfer query ok".encode('utf-8'))
                except Exception as e:
                    print (e)

                print ("Recived size : {}".format(data_transferred))

        except Exception as e:
            print (e)
            self.connections.remove(self.connection)
            self.tcpServerThreads.remove(self)
            exit(0)
        self.connections.remove(self.connection)
        self.tcpServerThreads.remove(self)


    def send(self, message):
        print('tcp server :: ', message)
        try:
            for i in range(len(self.connections)):
                self.connections[i].sendall(message.encode())
        except:
            pass
