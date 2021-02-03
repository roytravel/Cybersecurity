# -*- coding:utf-8 -*-

import os
import sys
import hashlib
import argparse
import pefile
from datetime import datetime



def HASH_CALCULATE(path):
    with open(path,'rb') as BinaryFile:

        binFile = BinaryFile.read()
        md5 = hashlib.md5(binFile)
        sha1 = hashlib.sha1(binFile)
        sha256 = hashlib.sha256(binFile)

        print ("[HASH VALUE]")
        print ("→ MD5    : {}".format(md5.hexdigest()))
        print ("→ SHA1   : {}".format(sha1.hexdigest()))
        print ("→ SHA256 : {}".format(sha256.hexdigest()))
        print ("\n"),
    


def IMAGE_DOS_HEADER():

    e_magic = hex(data.DOS_HEADER.e_magic)
    e_lfanew = hex(data.DOS_HEADER.e_lfanew) 
    print ("[IMAGE DOS HEADER]")

    if e_magic == '0x5a4d': 
        print ("→ PE OFFSET : ",e_lfanew)
    if e_magic != '0x5a4d': 
        print ("→ THIS IS NOT PE STRUCTURE")
    print ("\n"),



def IMAGE_FILE_HEADER():

    Machine = data.FILE_HEADER.Machine
    Section = data.FILE_HEADER.NumberOfSections
    timeDateStamp = data.FILE_HEADER.TimeDateStamp
    sizeOfOptionalHeader = data.FILE_HEADER.SizeOfOptionalHeader
    characteristic = data.FILE_HEADER.Characteristics

    print ("[IMAGE FILE HEADER]")

    if Machine == 0x14c:
        print ("→ TARGET MACHINE : i386")
    if Machine == 0x8664:
        print ("→ TARGET MACHINE : AMD64")

    print ("→ COMPILE TIME   : {}".format(datetime.fromtimestamp(timeDateStamp)))
    print ("→ SECTION COUNT  : {}".format(Section))

    if sizeOfOptionalHeader == 0xe0 :
        print ("→ SIZE OF OPTIONAL HEADER : 32bit")
    if sizeOfOptionalHeader == 0xf0 :
        print ("→ SIZE OF OPTIONAL HEADER : 64bit")
    if characteristic == 0x102 :
        print ("→ CHRACTERISTICS : 32bit executable")
    print ("\n"),



def IMAGE_OPTIONAL_HEADER():

    Magic = data.OPTIONAL_HEADER.Magic
    sizeOfCode = data.OPTIONAL_HEADER.SizeOfCode
    entryPoint = hex(data.OPTIONAL_HEADER.AddressOfEntryPoint)
    baseOfCode = hex(data.OPTIONAL_HEADER.BaseOfCode) #코드 영역이 시작되는 상대주소(RVA) // ImageBase + BaseOfCode = 실제 코드 영역
    imageBase = hex(data.OPTIONAL_HEADER.ImageBase)
    sectionAlignment = hex(data.OPTIONAL_HEADER.SectionAlignment)
    fileAlignment = hex(data.OPTIONAL_HEADER.FileAlignment)

    #1. PE 파일이 메모리에 로딩되었을 때 전체 크기,
    #2. 로딩 후 SectionAlignment의 영향으로 패딩이 붙음
    #3. SizeOfImage 또한 SectionAlignment의 영향을 받음
    sizeOfImage = hex(data.OPTIONAL_HEADER.SizeOfImage) 
    subSystem = hex(data.OPTIONAL_HEADER.Subsystem)

    print ("[IMAGE OPTIONAL HEADER]")
    print ("→ SIZE OF CODE      : {}".format(hex(sizeOfCode)))
    print ("→ ENTRY POINT       : {}".format(entryPoint))
    print ("→ BASE OF CODE      : {}".format(baseOfCode))
    print ("→ IMAGE BASE        : {}".format(imageBase))
    print ("→ SECTION ALIGNMENT : {}".format(sectionAlignment))
    print ("→ FILE ALIGNMENT    : {}".format(fileAlignment))
    print ("→ SIZE OF IMAGE     : {}".format(sizeOfImage))

    if subSystem == 0x01 : print ("→ SUBSYSTEM : System Driver File")
    if subSystem == 0x02 : print ("→ SUBSYSTEM : GUI Program")
    if subSystem == 0x03 : print ("→ SUBSYSTEM : CLI Program")
    if Magic == 0x10B : print ("→ STRUCTURE : PE32")
    if Magic == 0x20B : print ("→ STRUCTURE : PE32+")
    print ("\n"),



def IMAGE_SECTION_HEADER():

    print ("[IMAGE SECTION HEADER]")
    print ("----------------------------------------------------------------------------------------------------------")
    print ("|  NAME  | Virtual Addr | Virtual Size | Raw Data | Raw Size | Entropy |  MD5                             |")
    print ("-----------------------------------------------------------------------------------------------------------")

    for section in data.sections:

        print ("→",section.Name.decode('utf-8').ljust(8), hex(section.VirtualAddress).ljust(14), hex(section.Misc_VirtualSize).ljust(14),
        hex(section.PointerToRawData).ljust(10),hex(section.SizeOfRawData).ljust(10),round(section.get_entropy(),2),"".ljust(4),section.get_hash_md5())



def DIRECTORY_ENTRY_IMPORT(fullPath):
    try:
        for entry in data.DIRECTORY_ENTRY_IMPORT:
            with open(fullPath + "_Import.txt", "a") as DLL:
                DLL.write(entry.dll.decode('utf-8'))
                DLL.write('\n',)
                for API in entry.imports:
                    try:
                        DLL.write(API.name.decode('utf-8'))
                        DLL.write('\n',)
                    except Exception as e:
                        pass
                DLL.write('\n',)
        print ("[+] Completed : {}".format(fullPath))
    except Exception as e:
        print ("[!] {} : {}".format(fullPath,e))
        with open(root+"Error.txt",'a') as err:
            err.write(fullPath)
            err.write('\n')
        pass


if __name__ == '__main__':

    parser=argparse.ArgumentParser(add_help=True)
    parser.add_argument('-f',action='store',dest='file',help='File') 
    parser.add_argument('-d',action='store',dest='dir',help='Directory')
    parser.add_argument('--mod-file',action='store',dest='mf',help='Extract DLL and API in file')
    parser.add_argument('--mod-dir',action='store',dest='md',help='Extract DLL and API in files')
    args=parser.parse_args()


    #Ex) Python peParser.py -f C:/Sample/exe32/000bc2a12fec3a2099816f65c2f7341f
    if args.file != None:
        data = pefile.PE(args.file)
        HASH_CALCULATE(args.file)
        IMAGE_DOS_HEADER()
        IMAGE_FILE_HEADER()
        IMAGE_OPTIONAL_HEADER()
        IMAGE_SECTION_HEADER()


    #Ex) Python peParser.py -d C:/Sample/exe32/
    elif args.dir != None:
        for (root, dirs, files) in os.walk(args.dir):
            for fileName in files:
                fullPath = root + fileName
                data = pefile.PE(fullPath)
                HASH_CALCULATE(fullPath)
                IMAGE_DOS_HEADER()
                IMAGE_FILE_HEADER()
                IMAGE_OPTIONAL_HEADER()
                IMAGE_SECTION_HEADER()
                print ("\n---------------------------------------------------------------------------------------------------------")

    #Ex) Python peParser.py --mod-file C:/Sample/exe32/000bc2a12fec3a2099816f65c2f7341f
    elif args.mf != None:
        data = pefile.PE(args.mf)
        DIRECTORY_ENTRY_IMPORT(args.mf)

    #Ex) Python peParser.py --mod-dir C:/Sample/exe32/
    elif args.md != None:
        for (root, dirs, files) in os.walk(args.md):
            for fileName in files:
                fullPath = root + fileName
                data = pefile.PE(fullPath)
                DIRECTORY_ENTRY_IMPORT(fullPath)

