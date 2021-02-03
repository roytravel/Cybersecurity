# -*- coding:utf-8 -*-
import os
import argparse

def Argument():
    parser=argparse.ArgumentParser(add_help=True)
    parser.add_argument('-d',action='store',dest='dir',help='Directory')
    args=parser.parse_args()
    return (args)

def Modify(Directory): 
    # 디렉터리 및 파일 탐색
    for (root, dirs, files) in os.walk(Directory):
        root = root + "\\"

        #파일 인덱싱
        for idx in range(len(files)):

            #특정 파일 확장자 체크
            if files[idx].endswith("vir"):

                #특정 문자열 및 확장자 제거
                newName = files[idx].strip("_virussign.com_").strip(".vir")

                #원본 이름에서 새로운 이름으로 변경
                os.rename(root + files[idx] , root + newName)

if __name__ == "__main__":
    args = Argument()
    Modify(args.dir) #python ReName.py -d [DIRECTORY]
