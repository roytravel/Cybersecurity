# -*- coding:utf-8 -*-

import os
import sys
import pefile
import shutil
import argparse
import multiprocessing



PACKERS_FLAG = {
    #Checked Flag
        '.asp': 'ASP',
        '.ada': 'ARM',
        '.eco': 'EPL',
        '.eda': 'EPL',
        '.eni': 'ENI',
        '.mnb': 'MNB',
        '.MPR': 'MPR',
        '.neo': 'NEO',
        '.nsp': 'NSP',
        'nsp0': 'NSP',
        'nsp1': 'NSP',
        '.pet': 'PET',
        'pec1': 'PEC',
        'pec2': 'PEC',
        'pec3': 'PEC',
        'pec4': 'PEC',
        'pec5': 'PEC',
        'pec6': 'PEC',
        '.New' : 'NEW',
        'Them': 'THE',
        '.tsu': 'TSU',
        '.Upa': 'UPA',
        '.UPX': 'UPX',
        'UPX0' : 'UPX',
        'UPX1' : 'UPX',
        'UPX2' : 'UPX',
        '.vmp': 'VMP',
        '.rmn': 'RAM',
        '.\x00\x00\x00' : 'NUL',
        '\x00\x00\x00\x00' : 'NUL',
        '.RLI' : 'RLI',
        '_WIN' : 'WIN',

    #Unchecked Flag
        'ccg': 'CCG',
        'char': 'PPI',
        'BitA': 'CRU',
        'DASt': 'DAS',
        '!EPa': 'EPA',
        'FSG!': 'FSG',
        'kkru': 'KKR',
        'mack': 'ImpRec_created',
        'Mask': 'MAS',
        'MEW': 'MEW',        
        'pack': 'RLP',
        'PEBu': 'PEB',
        'PECo': 'PEC',
        'pec2': 'PEC',
        'PELO': 'PEL',
        'perp': 'PER',
        'PESH': 'PES',
        'pinc': 'PIN',
        'ProC': 'PRO',
        'RLPa': 'RLP',
        'RCry': 'RPC',
        'RPCr': 'RPC',
        'sfor': 'STA',
        'spac': 'SIM',
        'svkp': 'SVK',
        'PEPA': 'PEP',
        'ByDw': 'UPA',
        'VPro': 'VPR',
        'wina': 'API',
        'WinL': 'WIN',
        'WWPA': 'WWP',
        'yP': 'YOD',
        'y0da': 'YOD'
}



PACKERS_NAME = {
        'ASP': 'Aspack',
        'ARM': 'Armadillo',
        'EPL': 'EPL',
        'EPL': 'EPL',
        'ENI': 'Enigma',
        'MNB': 'Mnbvcx',
        'MPR': 'MPRESS',
        'NEO': 'Neolite',
        'NSP': 'Nspack',
        'PET': 'Petite',
        'PEC': 'PECompact',
        'NEW' : 'Newsec',
        'THE': 'Themida',
        'TSU': 'TSULoader',
        'UPA': 'Upack',
        'UPX': 'UPX',
        'VMP': 'Vmprotect',
        'RAM': 'Ramnit',
        'NUL' : 'NULL',
        'RLI' : 'RLICKY4',
        'WIN' : 'Winzip',

    #Unchecked
        'ccg': 'CCG',
        'char': 'PPI',
        'BitA': 'CRU',
        'DASt': 'DAS',
        '!EPa': 'EPA',
        'FSG!': 'FSG',
        'kkru': 'KKR',
        'mack': 'ImpRec_created',
        'Mask': 'MAS',
        'MEW': 'MEW',        
        'pack': 'RLP',
        'PEBu': 'PEB',
        'PECo': 'PEC',
        'pec2': 'PEC',
        'PELO': 'PEL',
        'perp': 'PER',
        'PESH': 'PES',
        'pinc': 'PIN',
        'ProC': 'PRO',
        'RLPa': 'RLP',
        'RCry': 'RPC',
        'RPCr': 'RPC',
        'sfor': 'STA',
        'spac': 'SIM',
        'svkp': 'SVK',
        'PEPA': 'PEP',
        'ByDw': 'UPA',
        'VPro': 'VPR',
        'wina': 'API',
        'WinL': 'WIN',
        'WWPA': 'WWP',
        'yP': 'YOD',
        'y0da': 'YOD'
}



def createDir(basePath):
    global baseDir
    baseDir = basePath
    otherList = ['ERROR','NORMAL','UNKNOWN','NULL']
    packList = ['Aspack','Armadillo','CCG','PPI','Crunch','DastubDragonArmorProtector','Enigma','Epack','EPL','FSG','kkrunchy','ImpRec_created','MaskPE',
    'MEW','Mnbvcx','MPRESS','neolite','Newsec','NsPack','RLPack','PEBundle','PECompact','PELock','Perplex','PEShield','Petite','ProCrypt','RLICKY4','Ramnit','RPCrypt',
    'StarForce','Simple','SVKP','Themida','TSULoader','Pepack','Upack','UPX','VMProtect','Vprotect','API_Override','WinLicense','WinZip','WWPACK','Y0da']

    if not os.path.isdir(baseDir):
        os.mkdir(baseDir)

    for packer in range(len(packList)):
        try:
            if not os.path.isdir(packList[packer]):
                os.mkdir(baseDir+packList[packer])
        except:
            pass

    for other in range(len(otherList)):
        try:
            if not os.path.isdir(otherList[other]):
                os.mkdir(baseDir+otherList[other])
        except:
            pass



def checkDirectory(wantToCheckDir):
    
    for (path, test, files) in os.walk(wantToCheckDir):
        for file in files:
            sectionName = list()

            fullpath = path + file
            binary = pefile.PE(fullpath)

            for section in binary.sections:
                sectionName.append(section.Name.decode('utf-8')[:4])
            
            print ("{} : {}".format(fullpath,sectionName))



def nullToEnigma(nullDirectory):
    
    for (path, test, files) in os.walk(nullDirectory):
        for file in files:
            sectionName = list()

            fullpath = path + file
            binary = pefile.PE(fullpath)

            for section in binary.sections:
                sectionName.append(section.Name.decode('utf-8')[:4])

            if ".eni" in sectionName:
                binary.close()
                shutil.move(fullpath,baseDir+"Enigma")
                print ("{} : {}".format(fullpath,sectionName))
                


def blackDetect(fullPath,binary):
    blackList = ['.asp','.ada','.eco','.eda','.eni','.mnb','.MPR','.neo','.nsp','nsp0','nsp1','.pet','pec1','pec2','pec3','pec4',
    'pec5','pec6','.New','Them','.tsu','.Upa','.UPX','UPX0','UPX1','UPX2','.vmp','.rmn','.RLI','_WIN','\x00\x00\x00','\x00\x00\x00\x00']
    sectionName = list()
    pack = False

    try:
        for section in binary.sections:
            sectionName.append(section.Name.decode('utf-8')[:4])
        
        for element in blackList:
            if element in sectionName:
                pack = True
    
        print ("{} : {} : {}".format(pack,fullPath,sectionName))
    except Exception as e:
        print ("{} {}".format(e,fullPath))


def multiProc(fullList,count):
    allocate = [count,16]
    processes = list()

    for loop in range(allocate[1]):
        process = multiprocessing.Process(target=whiteDetect, args=(fullList,allocate,loop))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    
def whiteDetect(fullList,allocate,count):
    size = int(allocate[0] / allocate[1])
    start = count * size
    end = ((count+1)*size,allocate[0])[count==(allocate[1]-1)]

    whiteList = ['.tex','.cod','.dat','.rsr','.rda','.ida','CODE','DATA','BSS\x00','.rel','.rcr','.bss','.rod',
        '.gfi','.uda','.hda','.ite','.nda','.imp','.tls',".xda",'.sda','.CRT','.sxd','.deb','.did','.eh_']

    while (True):
        try:

            for index in range(start,end):
                abnormal = False
                sectionName = list()
                binary = pefile.PE(fullList[index])
                
                for section in binary.sections:
                    sectionName.append(section.Name.decode('utf-8')[:4])

                for element in sectionName:

                    if (element not in whiteList) :
                        abnormal = True
                        break

                mutex = False

                #If there is abnormal section name
                if (abnormal):

                    # Check the Section Name
                    for name in sectionName:
                        if (name in PACKERS_FLAG) :
                            binary.close()
                            shutil.move(fullList[index], baseDir + PACKERS_NAME[PACKERS_FLAG[name]])
                            print ("{} : {} : {}".format(fullList[index],PACKERS_FLAG[name],sectionName))
                            mutex = True
                            break

                    if mutex :
                        pass

                    else :
                        binary.close()
                        shutil.move(fullList[index], baseDir + "UNKNOWN")
                        print ("{} : UNK :  {}".format(fullList[index],sectionName))

                else: 
                    binary.close()
                    shutil.move(fullList[index], baseDir + "NORMAL")
                    print ("{} : NOR : {}".format(fullList[index],sectionName))

        except Exception as e:
            binary.close()
            shutil.move(fullList[index], baseDir + "ERROR")
            print ("[!] {} : {}".format(e,fullList[index]))



if __name__ == '__main__':

    parser=argparse.ArgumentParser(add_help=True)
    parser.add_argument('-f',action='store',dest='file',help='File')
    parser.add_argument('-d',action='store',dest='dir',help='Directory')
    parser.add_argument('-c',action='store',dest='check',help='Want to check directory')
    args=parser.parse_args()


    if (len(sys.argv) != 3):
        print ("[packDetector.py -h]")

    if args.dir != None:
        createDir(args.dir)
        fullList = list()
        
        for (path, test, files) in os.walk(args.dir):
            for file in files:
                fullPath = path + file
                fullList.append(fullPath)
        
        multiProc(fullList,len(files))


    elif args.check != None:
        checkDirectory(args.check)
