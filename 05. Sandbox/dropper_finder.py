# -*- coding:utf-8 -*-

import os
import re
import sys
import pefile
import shutil
import argparse


peHeader = b'\x4D\x5A'
rsrcSection = b".rsrc\x00\x00\x00"


def mkdir(args):
    if not os.path.isdir(args.dir + "dropped"):
        os.mkdir(args.dir + "dropped")

    if not os.path.isdir(args.dir + "temporary"):
        os.mkdir(args.dir + "temporary")

    if not os.path.isdir(args.dir + "suspicious"):
        os.mkdir(args.dir + "suspicious")


def Argument():
    parser=argparse.ArgumentParser(add_help=True)
    parser.add_argument('-d',action='store',dest='dir',help='Directory')
    parser.add_argument('-c',action='store',dest='check',help='Checking suspicious directory')
    args=parser.parse_args()
    return args


def SearchFile(directory):
    fullPath = list()
    for root, dirs, files in os.walk(directory):        
        for fileName in files:
            full = root + fileName
            fullPath.append(full)
        return (fullPath)


def ExtractDropFile(fullPath,index,malware,peStart):
    try:
        #.rsrc 영역에 존재하는 내부 바이너리 PE 구조의 시작으로부터 1024바이트 읽고 바이너리로 저장
        with open(fullPath[index] + "_temporary", 'wb') as saveTmp:
            saveTmp.write(malware.read(1024))
        
        #저장한 내부 바이너리를 읽어들인 후 pefile 모듈의 인자로 전달
        with open(fullPath[index] + "_temporary", 'rb') as readTmp:
            readTmp = pefile.PE(fullPath[index] + "_temporary")

            #내부 바이너리의 마지막 섹션의 시작 오프셋과 크기를 구함
            for _section in readTmp.sections:
                offset = _section.PointerToRawData
                size = _section.SizeOfRawData
            
            #마지막 섹션의 시작 오프셋과 크기를 더함으로써 내부 바이너리 PE 구조의 끝을 계산
            volume = offset + size

            #내부 바이너리 PE 구조의 시작점으로 이동
            malware.seek(int(peStart,16))
        
        #내부 바이너리의 PE 구조의 시작부터 끝(volume)까지 읽어들여 내부 바이너리 추출
        with open(fullPath[index]+"_dropped", 'wb') as dropFile:
            dropFile.write(malware.read(volume))
            print ("[+] Found another binary --> {} : {} ".format(fullPath[index],peStart))

    except Exception as e:
        # print (e,fullPath[index])
        os.rename(fullPath[index] + "_temporary", fullPath[index] + "_suspicious")


def FindAnotherPE(fullPath):

    #배열 변수 fullPath에 존재하는 바이너리 파일을 pefile 모듈의 인자로 전달
    for index in range(len(fullPath)):
        binary = pefile.PE(fullPath[index])

        #바이너리의 IMAGE_SECTION_HEADER 구조체에서 Name 값이 .rsrc인 Section을 찾음
        for section in binary.sections:
            if section.Name == rsrcSection: 
                
                #.rsrc인 Section을 찾고 해당 Section의 Offset으로 이동한 뒤 Section의 크기 만큼 읽어 들임
                with open(fullPath[index], 'rb') as malware:
                    malware.seek(section.PointerToRawData)
                    IsDropFile = malware.read(section.SizeOfRawData)

                    #Section의 크기 만큼 읽어들인 데이터 속에 PE 구조의 헤더가 존재하는지 확인하고 바이너리 내부의 또다른 바이너리의 시작 오프셋 구함
                    if (peHeader in IsDropFile) :
                        peStart = hex(int(hex(section.PointerToRawData),16) + int(hex(IsDropFile.find(peHeader)),16))
                        malware.seek(int(peStart,16))
                        ExtractDropFile(fullPath,index,malware,peStart)


def checkHiddenPE(args):

    #susp 디렉터리를 탐색하여 모든 파일에 대한 전체 경로가 담긴 리스트 반환
    fullPath = SearchFile(args.check)
    
    #susp 디렉터리에서 확인된 바이너리를 읽음
    for index in range(len(fullPath)):
        with open(fullPath[index], 'rb') as malware:
            binary = malware.read()

            #특정 문자열(MZ)이 여러번 포함된 경우를 찾음
            Signature = [m.start() for m in re.finditer(b'\x4D\x5A',binary)]
            
            #리스트 변수 Signature의 두 개 이상의 PE 시그니처가 존재할 경우
            if (len(Signature) > 1):

                #첫 번째 PE 시그니처를 제외한 모든 시그니처를 확인
                for idx in range(1, len(Signature)):

                    #PE 시그니처의 시작 위치로 이동
                    malware.seek(Signature[idx])

                    #PE의 시작부터 끝 지점까지 바이너리 지정
                    BinaryDump = malware.read(len(binary) - Signature[idx])

                    #지정한 바이너리 파일 이름 및 경로 지정
                    BinaryDumpPath = '{}_{}'.format(fullPath[index], Signature[idx])

                    #지정한 바이너리 데이터 저장
                    with open(BinaryDumpPath, 'wb') as dumpFile:
                        dumpFile.write(BinaryDump)

                    try:
                        with open(BinaryDumpPath, 'rb') as data:

                            #IMAGE_DOS_HEADER의 e_lfanew 값이 존재하는 위치로 이동
                            data.seek(0x3c)

                            #e_lfanew 값 읽기
                            e_lfanew = data.read(4)

                            #이동할 위치 값을 정수로 변환
                            offsetPE = int(e_lfanew[::-1].hex(),16)

                            #문자열 'PE'가 존재해야 할 위치로 이동
                            data.seek(offsetPE)

                            #PE가 존재해야 할 위치에서 2바이트를 읽음
                            isNamePE = data.read(2)
                            
                            #만약 'PE'라는 문자열이 존재할 경우 해당 파일 출력
                            if isNamePE ==b'\x50\x45':
                                print ("[+] Found Hidden PE File : {} ".format(BinaryDumpPath))
                            
                            else:
                                data.close()
                                os.remove(BinaryDumpPath)
                                pass
                    except Exception as e:
                        print (e)


def moveFile(args):
    print ("\n",)
    os.system("move {}*_temporary {}temporary".format(args.dir,args.dir))
    print ('\n',)
    os.system("move {}*_dropped {}dropped".format(args.dir,args.dir))
    print ('\n',)
    os.system('move {}*_suspicious {}suspicious'.format(args.dir,args.dir))


if __name__=="__main__" :
    
    #Add argument to set options
    args = Argument()


    if args.dir != None :

        #Create a dirctory to hold the dropped binary
        mkdir(args)

        #Ex) Python findDropper.py -d C:\Binary\exe32\NORMAL
        fullPath = SearchFile(args.dir)

        #Checking what file has another binary
        FindAnotherPE(fullPath)

        #Move each of extracted files and temporary files to drop, temp directory
        moveFile(args)

    if args.check != None :
        
        #Hidden multiple PE Structure check and extract
        checkHiddenPE(args)

