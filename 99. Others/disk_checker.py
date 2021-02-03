#! /usr/bin/python
import os

diskInfo = os.statvfs("/")


def get_disk_info(path):
    diskInfo = os.statvfs(path)
    return diskInfo


def get_disk_size(path):
    diskInfo = get_disk_info(path)
    total = diskInfo.f_bsize * diskInfo.f_blocks
    available = diskInfo.f_bsize * diskInfo.f_bavail
    used = diskInfo.f_bsize * (diskInfo.f_blocks - diskInfo.f_bavail)
    return total, available, used


if __name__ == '__main__':
    size = get_disk_size('/')
    available = size[1]/(1024**3)
    if (available <20):
        print ("No enough disk space, start clean cuckoo...")
        os.system("cuckoo clean")
    else:
        print ("Available Disk : {}GB".format(available))
