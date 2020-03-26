import pandas as pd

class DataFrame(object):

    def __init__(self):
        pass

    def get_value(self, df):
        value = df.values
        return value

    # getting the count of row and column
    def get_frame_shape(self, df):
        shape = df.shape
        return shape

    # getting the index: start, stop, step
    def get_index(self, df):
        index = df.index
        return index


    def get_infomation(self, df):
        infomation = df.info()
        return infomation

    # getting the count how many column has record
    def get_value_counts(self, df, column):
        count = df[column].value_counts()
        return count
        

    # getting the value of count, mean, std, min, max and so on.
    def get_describe(self, df):
        describe = df.describe()
        return describe

if __name__ == '__main__':

    Frame = DataFrame()
    xlsx = ['calc.xlsx', 'mspaint.xlsx', 'control.xlsx', 'explorer.xlsx', 'mmc(services.msc).xlsx', 'notepad.xlsx']

    for index in range(len(xlsx)):
        dFrame = pd.read_excel(xlsx[index])
        print ("[+] {}".format(xlsx[index]))


        test = Frame.get_value_counts(dFrame, 'Full Category').head(60)
        print (test)
        
        # test = dFrame[dFrame['Module']=="win32calc.exe"]['API'].tolist()
        # for i in range(len(test)):
        #     print (test[i])
        break
