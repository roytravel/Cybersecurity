import rstparse
import os

def get_pst_file():
    for (root, dirs, files) in os.walk("C:/sigs"):
        fullpath = list()
        root = root + '/'
        for file in files:
            path = root + file
            fullpath.append(path)
    return fullpath


def get_pst_data(fullpath):
    api_list = list()

    # PST 파일을 하나씩 인덱싱
    for index in range(len(fullpath)):

        # 인덱싱한 파일을 차례대로 Read
        with open(fullpath[index]) as file:
            rst.read(file)
            rst.parse()
        
        ## 각 파일의 모든 lines을 enumerate
        # for i, line in enumerate(rst.lines):
            # if ("==") in line:
            #     api_list.append(rst.lines[i-1])
            # api_list.append("Signature::")
            # api_list.append("Flags::")
        
        # DLL과 API 세트를 담을 리스트 생성
        temp = list()
        for i, line in enumerate(rst.lines):
            
            if ("==") in line:
                api = rst.lines[i-1]

            if ("* Library") in line:
                library = line.split('* Library: ')
                if "." not in library[1]:
                    if "_" in library[1]:
                        dll = library[1]
                    else:
                        dll = library[1] + ".dll"
                else:
                    dll = library[1]

                one_set = dict(dll=dll, api=api)
                temp.append(one_set)


        
            # if ("* Return value:") in line:
            #     return_value = line.split("* Return value: ")
            #     print ("  [-] RET : {}".format(return_value[1]))

            # if ("Parameters::") in line:
            #     print ("  [-] PARAMETERS")
            #     try:
            #         for j in range(10):
            #             if (len(rst.lines[i+j]) != 0):
            #                 if (rst.lines[i+j] not in api_list):
            #                     if ("Parameters::") not in rst.lines[i+j]:
            #                         print (rst.lines[i+j])
                # except:
                #     pass

        for k in range(len(temp)):
            print (temp[k]['dll'], " : ", temp[k]['api'])
            

        if index == 0:
            break
        print (fullpath[index], index)
        

if __name__ =='__main__':

    # RST Parser 생성
    rst = rstparse.Parser()

    # RST 경로 파일 전체 리스트화
    fullpath = get_pst_file()
    
    # RST 파일 데이터 추출
    get_pst_data(fullpath)


