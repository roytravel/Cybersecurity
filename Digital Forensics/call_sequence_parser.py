import os
import pandas as pd
import json


# import label data
def read_csv():
    csv = pd.read_csv('C:/labels.csv')
    return csv


# drop column to see clearly.
def drop_column(csv):
    selected_csv = csv.drop(['subID','done','file_name','file_size','file_type'], axis=1, inplace=False)
    return selected_csv
    

# It need to edit
def get_cID_funName(selected_csv):
    for index in range(len(selected_csv)):
        cID = selected_csv['cID'][index]
        function_name = selected_csv['function_name'][index]

    return cID, function_name


def get_json(fileName):
    with open(fileName, mode = 'r') as file:
        json_data = json.load(file)
        # dump_data = json.dumps(json_data)
    return json_data


def json_signatures(json_data):

    # declare lists to return important elements in signatures column.
    element = list()
    elements = list()

    # count 'marks' to extract important elements.
    for i in range(len(json_data)):
        for j in range(len(json_data['signatures'][i]["marks"])):
            try:
                element = list()
                element.append(json_data['signatures'][i]["marks"][j]['call']['category'])
                element.append(json_data['signatures'][i]["marks"][j]['call']['api'])
                element.append(json_data['signatures'][i]["marks"][j]['call']['arguments'])
                element.append(json_data['signatures'][i]["marks"][j]['call']['flags'])
                elements.append(element)
            except:
                pass
    return elements


def json_static(json_data):

    data = json_data['static']['pe_imports']
    elements = list()
    
    for i in range(len(data)):
        element = list()
        element.append(json_data['static']['pe_imports'][i]['dll'])
        # print (json_data['static']['pe_imports'][i]['dll'])
        for j in range(len(data[i]['imports'])):
            element.append(data[i]['imports'][j])
            # print (data[i]['imports'][j])
        elements.append(element)
    return elements


def json_behavior(json_data):
    pass



if __name__ == '__main__':
    csv = read_csv()
    selected_csv = drop_column(csv)
    get_cID_funName(selected_csv)
    fileName = "<PATH>"
    json_data = get_json(fileName)

    elements = json_signatures(json_data)
    elements_2 = json_static(json_data)
    # elements_3 = json_behavior(json_data)
    
