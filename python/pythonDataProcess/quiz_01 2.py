# from bs4 import BeautifulSoup
# import numpy as np
# from pandas import DataFrame
#
#
# html = open('ex5-10.html', 'r', encoding="utf-8")
# soup = BeautifulSoup(html, 'html.parser')
#
# result=[]
# tbody = soup.select_one("tbody")
# tds = tbody.findAll('td')
# for data in tds:
#     result.append(data.text)
# print(result)
# print('-'*50)
# ###################################################
#
# # mydata = (np.arange(8).reshape(2 , 4)
# mydata = (np.array(result))
# reshapedata = mydata.reshape(4, 3)
# print(reshapedata)
# print('-'*50)
#
# mycolumns = ['이름', '국어', '영어']
# myframe = DataFrame(np.reshape(reshapedata), columns=mycolumns)
# print(myframe)
# print('-' * 50)
#
# df = myframe
# newdf = df.set_index(keys=['이름'])
# print(newdf)
# print('-' * 50)
##################################################

from bs4 import BeautifulSoup
from pandas import DataFrame as df
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'AppleGothic'

html = open('ex5-10.html', 'r', encoding="utf-8")
soup = BeautifulSoup(html, 'html.parser')

result = []
tbody = soup.select_one("tbody")
tds = tbody.findAll('td')
for data in tds:
    result.append(data.text)
print(result)
print('-'*50)

mycolumns = ['이름', '국어', '영어']

myframe = df(np.reshape(np.array(result),(4,3)),
columns=mycolumns)
myframe = myframe.set_index('이름')

myframe.astype(float).plot(kind='line', rot=0, title='score', legend=True)
print(myframe)

filename = 'scoreGraph.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + 'Saved...')

print(myframe)
print('-'*50)
plt.show()