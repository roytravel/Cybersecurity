# -*- coding:utf-8 -*-
from sklearn import metrics
import pandas as pd
import numpy as np


if __name__ == '__main__':
    # Paramter 설정
    DATA_DIR = './dataset/'
    ANSWER_FILE = 'answer.csv'
    submit_file = 'submit.csv'
    value = 'Abnormal' # (Attack or Abnormal)

    # 데이터 프레임 로드
    answer = pd.read_csv(DATA_DIR+ANSWER_FILE)
    submit = pd.read_csv(DATA_DIR+submit_file)

    try:
        pass
        ## 불필요한 데이터 프레임 제거
        # answer = answer.drop(['SubClass'], axis=1)
        # submit = submit.drop(['SubClass'], axis=1)
    except Exception as e:
        print (e)
        pass

    # 인덱스 설정 / Index(['Number', 'Class', 'SubClass'])
    sub_col = submit.columns
    col = sub_col[0]
    submit = submit.set_index(col)

    sub_cols2 = answer.columns
    col2 = sub_cols2[0]
    answer = answer.set_index(col2)   

    # 데이터 프레임 결합
    df = answer.join(submit, lsuffix='_true', rsuffix='_pred')

    # 데이터 프레임 값 치환
    df['Class_true'] = df['Class_true'].replace('Normal', 0)
    df['Class_true'] = df['Class_true'].replace(value, 1)
    df['Class_pred'] = df['Class_pred'].replace('Normal', 0)
    df['Class_pred']= df['Class_pred'].replace(value, 1)

    # 데이터 프레임 값 추출
    y_true = df['Class_true']
    y_pred = df['Class_pred']

    # F1-Score 계산
    print('[+] Preicsion :', metrics.precision_score(y_true, y_pred))
    print('[+] Accuracy :', metrics.accuracy_score(y_true, y_pred))
    print('[+] Recall :', metrics.recall_score(y_true, y_pred))
    print('[+] F1-Score :', metrics.f1_score(y_true, y_pred))
