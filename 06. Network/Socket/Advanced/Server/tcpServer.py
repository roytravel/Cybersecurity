# -*- coding:utf-8 -*-
import socket, threading
import tcpServerThread


class TCPServer(threading.Thread):
    def __init__(self, HOST, PORT):
        threading.Thread.__init__(self)

        self.HOST = HOST
        self.PORT = PORT

        # 소켓 객체 생성
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # HOST 주소와 PORT를 사용하는 인터페이스와 연결
        self.serverSocket.bind((self.HOST, self.PORT))

        # 사용자의 접속을 기다리는 단계로 넘어감
        self.serverSocket.listen(1)

        # 연결된 목록과 쓰레드를 관리하기 위한 리스트 생성
        self.connections = []
        self.tcpServerThreads = []

    def run(self):
        try:
            while True:
                print ('[+] Server wait...')

                #클라이언트의 접속 수락
                #누군가가 접속하여 연결되었을 때 비로소 결과 값이 return 되는 함수
                #누군가 접속하기 전까지 이 부분에서 멈춰있음. connection을 통해 앞으로 통신을 진행
                connection, clientAddress = self.serverSocket.accept()

                self.connections.append(connection)
                print ('[+] Conneted  : {}'.format(clientAddress))

                subThread = tcpServerThread.TCPServerThread(self.tcpServerThreads, self.connections, connection,
                                                            clientAddress)
                subThread.start()
                self.tcpServerThreads.append(subThread)
        except:
            print("[!] ServerThread error")

    def sendAll(self, message):
        try:
            self.tcpServerThreads[0].send(message)
        except:
            pass
