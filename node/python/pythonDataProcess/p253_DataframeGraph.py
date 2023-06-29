import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'AppleGothic'

filename = 'dataframeGraph.csv'
myframe = pd.read_csv(filename, encoding='euc-kr')

myframe = myframe.set_index(keys='name')
print(myframe)_
filename = 'dataframeGraph01.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' Saved... ')
plt.show()

