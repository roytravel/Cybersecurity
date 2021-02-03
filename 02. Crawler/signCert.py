# -*- coding:utf-8 -*-

import requests
import zipfile
import re
import pymysql
import time
from multiprocessing import *

address = ""
certPath = "C:/#Data/ServerInfo.txt"
downPath = "C:/#Cert/"


def getHTML(url):  # 동작 효율성을 위하여 웹 서버에 저장된 공인인증서 정보를 html을 파싱하여 텍스트로 저장
    result = requests.get(url)
    source = result.text
    with open(certPath, 'w') as f:
        f.write(source)


def getZIPNAME(certPath):  # 정규식을 사용하여 저장된 텍스트 파일에서 ZIP 파일 이름 추출
    with open(certPath, 'r') as f:
        text = f.read()
        zipName = re.findall(r"\"\d[0-9]{0,3}\.\d[0-9]{0,3}\.\d[0-9]{0,3}\.\d[0-9]{0,3}\.zip\"", text)
        return zipName


def getUPTIME(certPath):  # 정규식을 사용하여 지정된 텍스트 파일에서 피해시각 추출
    with open(certPath, 'r') as f:
        text = f.read()
        upTime = re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", text)
        return upTime


def saveDataInZip(zipName):  # ZIP 파일에 존재하는 signCert.cert 파일의 정보를 파싱하여 텍스트로 저장
        for index in range(len(zipName)):
            zipName[index] = zipName[index].replace('"', '')
            zipPath = downPath + zipName[index]
            with zipfile.ZipFile(zipPath) as certZip:
                with certZip.open('signCert.cert') as certFile:
                    certInfo = (certFile.read().decode('cp949'))+"\n"
                    with open("C:/#Data/CertInfo.txt", "a") as f:
                        f.write(certInfo)


def multiProc(zipName):
        allocate = [len(zipName), 20]
        processes = list()

        for loop in range(allocate[1]):
                process = Process(target=download, args=(zipName,allocate,loop))
                processes.append(process)
                process.start()
        for process in processes:
                process.join()


def download(zipName,allocate,cnt):
        size = int(allocate[0] / allocate[1])
        start = cnt * size
        end = ((cnt+1)*size,allocate[0])[cnt==19]
        while (True):
                try :
                        for index in range(start,end):
                                zipName[index] = zipName[index].replace('"','')
                                url = address + zipName[index]
                                with open(downPath+zipName[index],"wb") as certFile:
                                        response = requests.get(url)
                                        if response.status_code==200:
                                                certFile.write(response.content)
                                        else:
                                                print ("[!]Download Error : {}".format(zipName[index]))
                        break
                except Exception as e:
                        print(zipName[index])


def contentParsing(zipName, upTime): #정규식을 적용하여 인증서에 저장된 이름, 은행명, 계좌, 피해자 현재 소재지 정보만을 추출
    with open("C:/#Data/CertInfo.txt", "r") as f:
        line = f.read()
        name = re.findall(r"[ㄱ-ㅣ가-힣]+", line)
        account = re.findall(r"[0-9]{20}", line)
        bankName = re.findall(r",ou=[a-z]{2,8},", line)
        country = re.findall(r"kr",line)
        dbInsert(upTime, name, account, bankName, zipName,country)


def dbInsert(upTime, name, account, bankName, ip, country): #데이터베이스 및 테이블 생성과 인증서로부터 파싱한 데이터 입력

    conn = pymysql.connect(host='localhost', user='root', password='apmsetup',db='certInfo',charset='euckr')
    curs = conn.cursor()

    dbSQL = "create database certInfo DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;"
    curs.execute(dbSQL)

    useSQL = "use certInfo"
    curs.execute(useSQL)

    tbSQL = "create table data(idx int not null auto_increment, upTime varchar(30) not null,\
    name varchar(20) not null, bankName varchar(15) not null, account varchar(30) not null, \
    ip varchar(20) not null, country varchar(10) not null, primary key(idx)) DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;"
    curs.execute(tbSQL)

    for k in range(len(name)):
        bankName[k] = bankName[k].replace(',','').replace('ou=','')
        ip[k] = ip[k].replace('"','').replace('.zip','')
        insertSQL = "insert into data(idx, upTime, name, bankName, account, ip, country) values\
        ({},'{}','{}','{}','{}','{}','{}')".format(k+1, upTime[k], name[k], bankName[k], account[k], ip[k], country[k])
        curs.execute(insertSQL)


def main():
    getHTML(address)
    zipName = getZIPNAME(certPath)
    upTime = getUPTIME(certPath)
    multiProc(zipName)       
    saveDataInZip(zipName)
    contentParsing(zipName, upTime)


if __name__ == '__main__':
    main()
