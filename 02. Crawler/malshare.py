import requests
from datetime import datetime
import os
import sys

def bodyData(apiKey,md5):
    '''Return element for transfering HTTP POST request'''
    form = {
        'api_key' :apiKey,
        'action'    : 'getfile',
        'hash'     : md5
        }

    headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
    return form, headers


def getText(day):
    hashURL = "https://malshare.com/daily/{}/malshare_fileList.{}.txt".format(day,day)
    hashData = requests.get(hashURL)
    fullPath = '/Project/Malware/Malshare/Text/{}.txt'.format(day)
    
    if not os.path.isfile(fullPath):
        with open(fullPath, mode = "w+") as hashList:
            hashList.write(hashData.text)
    else:
        print ("[+] Already Existed : {}".format(day))
    return fullPath


def getHashList(fullPath):
    with open(fullPath, 'r') as hashList:
        data = hashList.readlines()
    return data


def saveMalware(response,savePath):
    with open(savePath, mode = 'wb+') as f:
        if response[:5] != b"Error":
            f.write(response)
            return True
        else:
            print ("[+] Over Amount of API Usage")
            return False


def getMalware(data,api_key,idx,day):
    if not idx:
        for index in range(len(data)):
            md5 = data[index].strip('\n')
            form, headers = bodyData(api_key,md5)
            url = "https://malshare.com/sampleshare.php?action=getfile&hash={}".format(md5)
            response = requests.post(url,headers=headers,data=form).content
            savePath = "/Project/Malware/Malshare/Sample/{}/{}.vir".format(day,md5)
            flag = saveMalware(response,savePath)
            if flag == False:
                return False, index
            if index % 49 == 0:
                print ("[+] Collected : ({}/{})".format(index+1,len(data)))
            if index == len(data)-1:
                print ("[+] Finished")
    else:
        for index in range(idx,len(data)):
            md5 = data[index].strip('\n')
            form, headers = bodyData(api_key,md5)
            url = "https://malshare.com/sampleshare.php?action=getfile&hash={}".format(md5)
            response = requests.post(url,headers=headers,data=form).content
            savePath = "/Project/Malware/Malshare/Sample/{}/{}.vir".format(day,md5)
            flag = saveMalware(response,savePath)
            if index == len(data)-1:
                print ("[+] Finished")
                return False, False
    
            if flag == False:
                return False, index

            if index % 49 == 0:
                print ("[+] Collected : ({}/{})".format(index+1,len(data)))



if __name__=='__main__':

    api_key = ['<API_KEY>','API_KEY']
    day = sys.argv[1]

    dirPath = '/Project/Malware/Malshare/Sample/{}'.format(day)
    if not os.path.isdir(dirPath):
        os.mkdir(dirPath)

    idx = ''
    for index in range(len(api_key)):
        fullPath = getText(day)
        data = getHashList(fullPath)
        flag, idx = getMalware(data,api_key[index],idx,day)
        
        if (flag == False) and (idx == False):
            break

        if flag == False:
            continue
