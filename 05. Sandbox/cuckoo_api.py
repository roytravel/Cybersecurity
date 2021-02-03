# -*- coding:utf-8 -*-
import os
import sys
import json
import requests
import time
import re
import coinaddr


class CUCKOO_API(object):
    
    @classmethod
    def __init__(self):
        self.API_SERVER = "http://192.168.36.130:8001"
        self.HEADERS = { 'Authorization': 'Bearer 7S-Uk0L94RWrdvfMnaxDnA',}
        self.SANDBOX = os.environ.get('SANDBOX')


    @classmethod
    def get_data_in_view(self,view):
        try:
            data = json.loads(view)
            taskID = data["task"]["guest"]["task_id"]
            target = data["task"]["target"].split('/')[-1]
            md5 = data["task"]["sample"]["md5"]
            sha256 = data["task"]["sample"]["sha256"]
            status = data["task"]["status"]
            return taskID, target, md5, sha256, status
        except Exception as error:
            return False, False, False, False, False


    @classmethod
    def view_file_request(self,index):
        REST_URI = "/files/view/id/{}".format(index)
        REST_URL = self.API_SERVER + REST_URI
        response = requests.get(REST_URL,headers=self.HEADERS).text
        return response


    @classmethod
    def get_file(self,sha256):
        REST_URI = "/files/get/{}".format(sha256)
        REST_URL = self.API_SERVER + REST_URI
        response = requests.get(REST_URL,headers=self.HEADERS).content
        return response


    @classmethod
    def tasks_view_request(self, index):
        REST_URI = "/tasks/view/{}".format(index)
        REST_URL = self.API_SERVER + REST_URI
        response = requests.get(REST_URL,headers=self.HEADERS).text
        view = (False, response)[not "Task not found" in response]
        return view


    @classmethod
    def memory_list_request(self,index):
        REST_URI = "/memory/list/{}".format(index)
        REST_URL = self.API_SERVER + REST_URI
        response = requests.get(REST_URL,headers=self.HEADERS).text
        if not "Memory dump not found" in response:
            data = json.loads(response)
            element = data["dump_files"]
            return element
        else:
            return False


    @classmethod
    def memory_get_request(self,index):
        REST_URI = "/memory/get/{}".format(index)
        REST_URL = self.API_SERVER + REST_URI
        response = requests.get(REST_URL,headers=self.HEADERS).content
        return response


    @classmethod
    def tasks_list_request(self):
        REST_URI = "/tasks/list"
        REST_URL = self.API_SERVER + REST_URI
        response = requests.get(REST_URL,headers=self.HEADERS).text
        tasks = json.loads(response)
        return tasks


    @classmethod
    def packet_dump_request(self,index,sha256):
        command = "curl -H 'Authorization: Bearer 7S-Uk0L94RWrdvfMnaxDnA' {}/pcap/get/{} > {}/packet/{}.pcap".format(self.API_SERVER, index,self.SANDBOX,sha256)
        os.system(command)


    @classmethod
    def report_request(self,index):
        try:
            REST_URI = "/tasks/report/{}".format(index)
            REST_URL = self.API_SERVER + REST_URI
            response = requests.get(REST_URL,headers=self.HEADERS)
            response = response.json()
            return response
        except:
            return False


    @classmethod
    def create_request(self,malware,machine):
        REST_URI = "/tasks/create/file"
        REST_URL = self.API_SERVER + REST_URI
        with open(malware, mode='rb') as sample:
            files = {"file" : (malware, sample)}
            machines = {'machine' : machine}
            requests.post(REST_URL, headers=self.HEADERS, files=files, data=machines)


    @classmethod
    def delete_request(self,index):
        REST_URI = "/tasks/delete/{}".format(index)
        REST_URL = self.API_SERVER + REST_URI
        requests.get(REST_URL, headers=self.HEADERS)


    @classmethod
    def get_task_id(self, tasks):
        task_id_list = list()
        try:
            for idx in range(len(tasks["tasks"])):
                try:
                    task_id_list.append(tasks["tasks"][idx]["guest"]['task_id'])
                except:
                    pass
            
            first_task_id = min(task_id_list)
            last_task_id = max(task_id_list)
            
            return first_task_id, last_task_id
        except:
            return False, False


    @classmethod
    def machine_view(self):
        REST_URI = "/machines/list"
        REST_URL = self.API_SERVER + REST_URI
        response = requests.get(REST_URL, headers=self.HEADERS).json()
        return response
