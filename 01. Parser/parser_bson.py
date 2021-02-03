import bson
import os


def get_fullpath():
    for root, dirs, files in os.walk("<PATH>"):
        fullpath = list()
        root = root + '/'
        for file in files:
            path = root + file
            fullpath.append(path)
    return fullpath


def extract_bson(fullpath):
    for index in range(len(fullpath)):
        with open(fullpath[index], 'rb') as bson_file:
            data = bson.decode_all(bson_file.read())
            print ("[+] {}".format(fullpath[index]))

            for j in range(len(data)):
                try:
                    print (data[j]['name'])
                except:
                    pass
            
            print ('\n\n')

    
if __name__ == '__main__':
    fullpath = get_fullpath()
    extract_bson(fullpath)
