# import bson
# import collections

# from bson.codec_options import CodecOptions

# data = bson.BSON.encode({'a':1})
# print (data)

# data = open('./bson/132.bson', 'rb')
# decoded_doc = bson.BSON(data).decode()
# print (decoded_doc)
# options = CodecOptions(document_class=collections.OrderedDict)

import bsonjs
import bson
import os

for root, dirs, files in os.walk("./bson"):
    test = list()
    root = root + '/'
    for file in files:
        fullpath = root + file
        test.append(fullpath)


# for index in range(len(test)):
    # with open(test[index], 'rb') as bson_file:
with open('./bson/1976.bson', 'rb') as bson_file:
    data = bson.decode_all(bson_file.read())
    # print ("[+] {}".format(test[index]))
    for j in range(len(data)):
        try:
            # if (data[j]['I']==45):
            #     print (data[j])
            print (data[j])

        except Exception as err:
            pass
        
        


