# -*- coding:utf-8 -*-

'''
Date - 2017.10.23
'''

import struct

#Check Bit
def checkBit(value):
    if value == "e000":
        print "\tSize Of Optional Header = 32bit"
    elif value == "f000":
        print "\tSize Of Optional Header = 64bit"
    else:
        print "\tI Don't know what is this"


#Check Machine
def mCheck(hex):
    if hex == "6486":
        print "\tMachine = " + "AMD64"
    elif hex == "4c01":
        print "\tMachine = " + "Intel386"

#Print Section Infomation
def secinfo(f):
    print "\tName = ", f.read(8).encode('ascii')
    print "\tVirtualSize = " + "0x" + f.read(4)[::-1].encode('hex').upper()
    print "\tVirtualAddress = " + "0x" + f.read(4)[::-1].encode('hex').upper()
    f.seek(24, 1)
    space()


#Line Feed
def space():
    print "\n",


def parser(filepath):
    with open(filepath, 'rb') as f:
        space()
        print "[+] Only 32Bit Program Can Parse"
        print "[+] Parsing Start = ", filepath
        space()

        #[IMAGE_DOS_HEADER]
        print "[IMAGE_DOS_HEADER]"
        e_magic = f.read(2)
        print "\tHeader Signature = " + e_magic
        f.seek(60)
        e_lfanew = f.read(4)
        print "\tOffset PE = " + "0x" + e_lfanew[::-1].encode('hex')
        space()

        #[IMAGE_FILE_HEADER]
        print "[IMAGE_FILE_HEADER]"
        startpe = struct.unpack("<L", e_lfanew)[0]
        f.seek(startpe)
        print "\tSignature = " + f.read(4)
        machine = f.read(2).encode('hex')
        mCheck(machine)
        nSection = f.read(2)[::-1].encode("hex")
        if nSection == "000a":
            nSection = 10
        else:
            print "\tNumber Of Sections = ", int(nSection)
        f.seek(12, 1)
        bit = f.read(2).encode('hex')
        checkBit(bit)  # 32 | 64 bit
        space()

        #[IMAGE_OPTIONAL_HEADER]
        print "[IMAGE_OPTIONAL_HEADER]"
        f.seek(18, 1)
        oep = f.read(4)[::-1].encode('hex')
        print "\tAddress Of Entry Point = ", "0x" + oep.upper()
        f.seek(8, 1)
        imgbase = f.read(4)[::-1].encode('hex')
        print "\tImageBase = " + "0x" + imgbase
        space()

        #[SectionTable]
        print "[SectionTable]"
        f.seek(192, 1)
        for i in range(int(nSection)):
            secinfo(f)

print "PATH :",
path = raw_input('')
parser(path)
