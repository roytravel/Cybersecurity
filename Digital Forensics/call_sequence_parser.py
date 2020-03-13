import os
import pandas as pd
import json


class Label(object):
    def __init__(self):
        pass


    # Read labels data to extract column
    def read_csv(self):
        csv = pd.read_csv('C:/labels.csv')
        return csv


    # Drop column to see clearly.
    def drop_column(self, csv):
        selected_csv = csv.drop(['subID','done','file_name','file_size','file_type'], axis=1, inplace=False)
        return selected_csv
    
    
    # Parse CID and Category
    def get_cID_funName(self, selected_csv):
        category = ['infostealer','keylogger','ransomware','stealth','worm']
        selection = list()
        for index in range(len(selected_csv)):
            if (selected_csv['function_name'][index] in category):
                cID = selected_csv['cID'][index]
                function_name = selected_csv['function_name'][index]
                selection.append(dict(cid = cID, function_name = function_name))            
        return selection



class Extract(object):
    def __init__(self):
        pass


    # Convert type of data to json
    def get_json(self, reportPath):
        with open(reportPath, mode = 'r') as file:
            json_data = json.load(file)
        return json_data


    # Extract category, api, arguments, flags
    def json_signatures(self, json_data):
        element = list()
        elements = list()

        for i in range(len(json_data)):
            try:
                for j in range(len(json_data['signatures'][i]["marks"])):
                        element = list()
                        element.append(json_data['signatures'][i]["marks"][j]['call']['category'])
                        element.append(json_data['signatures'][i]["marks"][j]['call']['api'])
                        element.append(json_data['signatures'][i]["marks"][j]['call']['arguments'])
                        element.append(json_data['signatures'][i]["marks"][j]['call']['flags'])
                        elements.append(element)
            except:
                pass
        return elements


    # Extract DLL and API
    def json_static(self, json_data):
        data = json_data['static']['pe_imports']
        elements = list()
        
        for i in range(len(data)):
            element = list()
            element.append(json_data['static']['pe_imports'][i]['dll'])
            for j in range(len(data[i]['imports'])):
                element.append(data[i]['imports'][j])
            elements.append(element)
        return elements


    # Extract category, api, arguments, flags
    def json_behavior(self, json_data):
        element = list()
        elements = list()

        # It need to handle and extract
        data = json_data['behavior']['apistats']

        for i in range(len(json_data['behavior']['processes'])):
            for j in range(len(json_data['behavior']['processes'][i])):
                try:
                    element = list()
                    element.append(json_data['behavior']['processes'][i]['calls'][j]['category'])
                    element.append(json_data['behavior']['processes'][i]['calls'][j]['api'])
                    element.append(json_data['behavior']['processes'][i]['calls'][j]['arguments'])
                    element.append(json_data['behavior']['processes'][i]['calls'][j]['flags'])
                    elements.append(element)
                except:
                    pass
        return elements


if __name__ == '__main__':

    Label = Label()
    Extract = Extract()

    csv = Label.read_csv()
    selected_csv = Label.drop_column(csv)
    selection = Label.get_cID_funName(selected_csv)

    
    
    for i in range(len(selection)):        
        key = list(selection[i].values())[0]
        values = list(selection[i].values())[1]
        reportPath = "<PATH>" + str(key)
        json_data = Extract.get_json(reportPath)



        # elements_1 = Extract.json_signatures(json_data)
        # for i in range(len(elements_1)):
        #     print (elements_1[i])

        # elements_2 = Extract.json_static(json_data)
        # for i in range(len(elements_2)):
        #     for j in range(len(elements_2[i])):
        #         print (elements_2[i][j])
          
        # elements_3 = Extract.json_behavior(json_data)
        # for i in range(len(elements_3)):
        #     print (elements_3[i])

