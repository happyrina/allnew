#판다스 기초
from pandas import DataFrame as dp
import numpy as np

mydata = np.arange(9).reshape((3, 3))
myframe = dp(data=mydata, index=['용산구', '마포구', '은평구'], columns=['김철수', '이영희', '정준수'])
print(myframe)
print('-' * 50)


#index를 안사용홰쑈기 때문에 행이 0과 1로 나타남
sdata = {'지역' : ['용산구', '마포구'], '연도': [2019, 2020]}
myframe = dp(data=sdata)
print(myframe)
print('-' * 50)

#중첩되어있는 Data
sdata = {'용산구' : {2020:10,2021:20},'마포구': {2020:30, 2021:40, 2022:50}}
myframe = dp(data=sdata)
print(myframe)
print('-'* 50)

sdata = {'지역' : ['용산구', '마포구', '용산구', '마포구', '마포구'], '연도': [2019, 2020, 2021, 2020, 2021], '실적': [20, 30, 35, 25, 45]}
myframe = dp(data=sdata)
print(myframe)
print('-' * 50)