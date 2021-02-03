# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
import argparse
import struct  # read method resolution
import os  # 많은 기능 중 폴더를 열수 있게 끔 해주는 기능이 있는 라이브러리


# 시간 변환 함수
def Trans_time(big):
    little = ''  # 빈 변수 할당
    for i in range(0, len(big), 2):
        little += big[-(i + 2)]
        little += big[-(i + 1)]
    return str(datetime(1601, 1, 1) + timedelta(microseconds=(int(little, 16) / 10), hours=+9))


# Prefetch File Header Structure
pfHeader = dict(version=0, size=0, name=0, hash=0, last_launch=0, launch_count=0)


def Display():
    print u'운영체제 버전 : ', pfHeader['version']
    print u'파일 사이즈 : ', pfHeader['size'], "BYTE"
    print u'파일 이름 : ', pfHeader['name']
    print u'경로 해시  : %X' % (pfHeader['hash'])
    print u'파일 실행 횟수 : ', pfHeader['launch_count']
    print u'최종실행 시각  : ', pfHeader['time']
    print '\n'


# OPERATING SYSTEM CHECK FUNCTION
def checkOS(version):
    if version == 17:
        return "WindowsXP"
    elif version == 23:
        return "Windows7"
    elif version == 26:
        return "Windows8"


# read라는 인자를 받아 PreFtech 파일의 구조를 해석함
def Parse(read):
    pfHeader['version'] = checkOS(struct.unpack('<L', read[0x00:0x04])[0])  # version  #<L = 4byte
    pfHeader['size'] = struct.unpack('<L', read[0x0c:0x10])[0]  # file size
    pfHeader['name'] = struct.unpack('58s', read[0x10:0x4A])[0].split('\x00\x00')[0].replace('\x00', '')
    pfHeader['hash'] = struct.unpack('<L', read[0x4C:0x50])[0]

    if pfHeader['version'] == "WindowsXP":
        pfHeader['count'] = struct.unpack('<L', read[0x90:0x94])[0]
        pfHeader['time'] = Trans_time(read[0x78:0x80].encode("hex"))

    if pfHeader['version'] == "Windows7":
        pfHeader['count'] = struct.unpack('<L', read[0x98:0x9C])[0]
        pfHeader['time'] = Trans_time(read[0x80:0x88].encode("hex"))

    if pfHeader['version'] == "Windows8":
        pfHeader['count'] = struct.unpack('<L', read[0xD0:0xD4])[0]
        pfHeader['time'] = Trans_time(read[0x80:0x88].encode("hex"))


if __name__ == "__main__":  # 본 코드 자체로만 동작할 때는 아래 코드가 메인 코드로 동작 // #만약 라이브러리 형태라면 아래 코드는 동작하지 않음
    parser = argparse.ArgumentParser(add_help=True)  # help 옵션 추가
    parser.add_argument('-f', action='store', dest='file', help='Parsing Prefetch File')  # 파일 파싱을 위한 옵션 추가
    parser.add_argument('-d', action='store', dest='dir', help='Parsing Prefetch File')  # 디렉토리를 파싱을 위한 옵션 추가
    args = parser.parse_args()

    if args.file != None:
        with open(args.file, 'rb') as f:  # 파일 열기
            Parse(f.read())  # 연 파일에 대한 읽기.
            Display()

    elif args.dir != None:  # 디렉토리가 있다면
        for (path, dir, files) in os.walk(args.dir):  # os 모듈을 이용해서 디렉토리 안으로 들어감
            for filename in files:
                with open(path + '\\' + filename, 'rb') as f:  # 파일 열기
                    Parse(f.read())  # 연 파일에 대한 읽기.
                    Display()
