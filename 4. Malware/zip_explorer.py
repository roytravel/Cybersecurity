# -*- coding:utf-8 -*-

import zipfile
import hashlib
import os
import sys
import time
import sqlite3


def dbInitiation():
    '''Create database file and Return connect, cursor'''
    connect = sqlite3.connect("/data/database/malware.db")
    cursor = connect.cursor()
    return connect, cursor


def tableCheck(connect, cursor):
    '''Check table that will contain hash value of malware is exist'''
    checkQuery = "SELECT COUNT(*) FROM sqlite_master WHERE name='hashinfo'"
    checkResult = cursor.execute(checkQuery)
    Flag = checkResult.fetchall()[0][0]
    return Flag


def tableCreate(connect, cursor, Flag):
    '''Create table that will contain hash value of malware'''
    if Flag is 0:
        SQL = "CREATE TABLE hashinfo(zipName varchar(42) not null, md5 char(32) not null, sha256 char(64) not null, primary key(sha256))"
        cursor.execute(SQL)


def checkIsProcessed():
    '''Collect *.zip.txt file what process completed already '''
    ProcessedList = list()
    for (root, dirs, files) in os.walk("/data/result/"):
        for file in files:
            file = "/data/hdd2t/" + file
            ProcessedList.append(file)
    return ProcessedList


def deleteExtention(ProcessedList):
    '''Remove exntention named ".txt" in *.zip.txt file list'''
    NewProcessedList = list()
    for index in range(len(ProcessedList)):
        NewProcessedList.append(ProcessedList[index].strip(".txt"))
    return NewProcessedList


def getZipName(rootDirectory,NewProcessedList):
    '''File Listing what exist in EC2 Malware Instnace'''
    zipFileList = list()
    for (root, dirs, zipFiles) in os.walk(rootDirectory):
        for zipFile in zipFiles:
            fullPath = root + zipFile
            if (zipFile.endswith('.zip')) and ("metadata" not in zipFile) and ("Android" not in zipFile):
                zipFileList.append(fullPath)

    for index in range(len(NewProcessedList)):
        if (NewProcessedList[index] in zipFileList):
            zipFileList.remove(NewProcessedList[index])
    return zipFileList, zipFiles


def getNameListInZip(index, zipFileList):
    '''Return list what file and directory path in internal zip file'''
    try:
        with zipfile.ZipFile(zipFileList[index]) as malwareZip:
            CompressData = zipfile.ZipFile(zipFileList[index])
            CompressDataNameList = malwareZip.namelist()
            return CompressDataNameList, CompressData
    except Exception as e:
        return False, False


def deleteElementDir(CompressDataNameList):
    '''Delete element that is not file(directory : yes) in ZIP file'''
    removeList = list()
    for count in range(len(CompressDataNameList)):
        if ".vir" not in CompressDataNameList[count]:
            removeList.append(count)
    NewCompressDataNameList = [i for j, i in enumerate(CompressDataNameList) if j not in removeList]
    return NewCompressDataNameList


def getFileHashInZip(NewCompressDataNameList,malwareZip):
    '''Calculate hash and return hash list in internal ZIP file'''
    hashSHA256 = list()
    hashMD5 = list()
    for index in range(len(NewCompressDataNameList)):
        if NewCompressDataNameList[index].endswith(".vir"):
            try:
                with malwareZip.open(NewCompressDataNameList[index]) as malware:
                    malwareByte = malware.read()
                hashMD5.append(hashlib.md5(malwareByte).hexdigest())
                hashSHA256.append(hashlib.sha256(malwareByte).hexdigest())
            except:
                continue
    return hashSHA256, hashMD5


def SaveHashLog(hashSHA256, hashMD5, zipFileName):
    '''Save hash value list in ZIP file as a text file'''
    zipFileName = zipFileName.strip("/data/hdd2t/")
    savePath = "/data/result/{}.txt".format(zipFileName)
    for index in range(len(hashSHA256)):
        with open(savePath, 'a+') as hashtxt:
            hashtxt.write(hashMD5[index]+":"+hashSHA256[index])
            hashtxt.write('\n')
    return savePath


def ValueRead(connect, cursor, readList):
    '''Read hash in log file list'''
    try:
        with open(readList,'r') as hashValue:
            hashValueList = hashValue.readlines()
        for count in range(len(hashValueList)):
            HashAlgorithm = hashValueList[count].split(":")
            zipName = readList.strip("/data/result/").strip(".txt")
            ValueInsert(connect, cursor, zipName, HashAlgorithm)
    except Exception as e:
        print (e)
        pass


def ValueInsert(connect, cursor, zipName, HashAlgorithm):
    '''Insert hash to hashinfo table'''
    try:
        InsertQuery = "insert into hashinfo(zipName, md5, sha256) values('{}','{}','{}')".format(zipName, HashAlgorithm[0], HashAlgorithm[1].strip(chr(0xa)))
        cursor.execute(InsertQuery)
        connect.commit()
    except Exception as e:
        print (e)
        pass


def main(Argumnet):
    '''Operate as a main function'''
    try:
        connect, cursor = dbInitiation()
        Flag = tableCheck(connect, cursor)
        tableCreate(connect, cursor, Flag)
        ProcessedList = checkIsProcessed()
        NewProcessedList = deleteExtention(ProcessedList)
        zipFileList, zipFiles = getZipName(Argument,NewProcessedList)

        for index in range(len(zipFileList)):
            print ("({}/{}) : {}".format(index+1,len(zipFileList),zipFileList[index]))
            CompressDataNameList, malwareZip = getNameListInZip(index, zipFileList)
            if (CompressDataNameList == False) and (malwareZip == False):
                continue
            NewCompressDataNameList = deleteElementDir(CompressDataNameList)
            hashSHA256, hashMD5 = getFileHashInZip(NewCompressDataNameList,malwareZip)
            savePath = SaveHashLog(hashSHA256, hashMD5, zipFileList[index])
            ValueRead(connect, cursor, savePath)
    except Exception as e:
        print (e)
        pass

if __name__ == "__main__":
    Argument = "/data/hdd2t/"
    main(Argument)
