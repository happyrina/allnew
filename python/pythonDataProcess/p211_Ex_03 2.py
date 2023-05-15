import numpy as np
import pandas as pd
from pandas import Series

filename = '과일매출현황.csv'

df = pd.read_csv(filename, index_col='과일명')
print('\n# 원본 데이터프레임')
print(df)

print('\n#누락 데이터 채워 넣기')
df.loc[df['구입액'].isnull(), '구입액'] = 50.00
df.loc[df['수입량'].isnull(), '수입량'] = 20.00
print(df)

print('\n#구입액과 수액량의 각 소계')
print(df.sum(axis=0))

print('\n#과일별 소계')
print(df.sum(axis=1))

print('\n구입액과 수입량의 평균')
print(df.mean())

print('\n과일별 평균')
print(df.mean(axis=1))