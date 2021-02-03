# -*- coding:utf-8 -*-

import os
import re


strings = r"A-Za-z0-9/\-:.,_$%'()[\]<> "

print ("[*] Input depth of strings : "),

length = int(raw_input())

regexp = '[%s]{%d,}' % (strings, length)

pattern = re.compile(regexp)


def Process(binary): #바이너리 상의 문자열 추출

    with open (binary, 'rb') as malware:

        data = malware.read()

        print pattern.findall(data)


def Search(Directory): #바이너리 전체 경로 확보 및 문자열 추출

    for (path, dir, files) in os.walk(Directory):

        path = path + "\\"

        for idx in range(len(files)):

            fullPath = path + files[idx]

            Process(fullPath)


if __name__ == "__main__":

    path = ""
    Search(path)
