import os

def get_text_file():
    fullpath = list()
    for (root, dirs, files) in os.walk("<PATH>"):
        root = root + '/'
        for file in files:
            path = root + file
            if ("default") in path:
                continue

            if ("COM") in path:
                continue
            fullpath.append(path)
    return fullpath


def change_all_line(fullpath, jndex, tmp):
    with open(fullpath[jndex], 'r',encoding='utf-16') as f:
        data = f.readlines()
        for kndex in range(len(data)):
            
            for mndex in range(0,len(tmp),2):
                if tmp[mndex+1] in data[kndex]:
                    print (tmp[mndex+1])


def splited_fullpath(fullpath,i):
    return fullpath[i].split('/')


if __name__ =='__main__':
    fullpath = get_text_file()
    splited_path = list()
    count=0
    test6 = list()
    # 전체 경로를 splited해서 나눔
    for i in range(len(fullpath)):
        splited_path.append(fullpath[i].split('/'))
    
    # rst에서 추출한 api 목록 파일을 엶
    with open('<RESULT TEXT FILE>', 'r') as f:

        #데이터를 줄단위로 읽고
        data = f.readlines()
        tmp = list()
        splited_data_list = list()

        # 모든 줄의 개수만큼 읽을건데 --로 시작하는건 제외해.
        for index in range(len(data)):
            if "--" in data[index]:
                continue

            #splited_data[0] = crypt32, splited_data[1] = CertOpenStore
            splited_data = data[index].split(':')

            # list안에 list가 들어감
            splited_data_list.append(splited_data)
        
        for j in range(len(splited_data_list)):
            
            #splited_path splited된 경로만큼 반복
            for k in range(len(splited_path)):
                if (splited_data_list[j][0]+".txt" == splited_path[k][-1].lower()):
                    if splited_data_list[j][1]!=splited_data_list[j-1][1]:
                        
                        test = str(splited_path[k][0]+'\\'+splited_path[k][1]+'\\'+splited_path[k][2]+'\\'+splited_path[k][3]+'\\'+splited_path[k][4]+'\\'+splited_path[k][5]+'\\'+splited_data_list[j][0]+".txt")

                        #각각 제대로 된 파일에 들어옴.
                        with open(test, 'r',encoding='utf-16le') as f:
                            data = f.readlines()

                            #모든 라인을 다 읽음
                            for m in range(len(data)):

                                #API 부분이 맞는지 비교
                                splited_data_list[j][1] = splited_data_list[j][1].replace('\n','')
                                test2 = data[m].split('(')

                                length = len(splited_data_list[j][1])
                                test3 = test2[0][-1:-length-1:-1]
                                test4 = list(test3)
                                test4.reverse()
                                test5 = ''.join(test4)
                                #맞는거까지해서 출력
                                if (splited_data_list[j][1] == test5):
                                    pathh = "<PATH RESULT>".format(test.split('\\')[-1])
                                    with open(pathh, "a+") as e:
                                        if data[m][0] == "!":
                                            data[m] = data[m][1:]
                                        e.write(data[m])
                                #     with open(test+"_", 'a+', encoding='utf-16le')  as e:
                                #         if data[m][0]== '!':
                                            
                                #             e.write(data[m][1:])
                                #         else:
                                #             e.write(data[m])
                                # else:
                                #     with open(test+"_", 'a+', encoding='utf-16le') as e:
                                #         if data[m][0]== '!':
                                #             e.write(data[m])
                                #         else:
                                #             data[m] = "!" + data[m]
                                #             e.write(data[m])
                                    

