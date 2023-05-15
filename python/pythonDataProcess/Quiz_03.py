import pandas as pd

afile = 'cheogajip.csv'
bfile = 'pelicana.csv'

atable = pd.read_csv(afile, index_col=0, encoding='utf-8')
btable = pd.read_csv(bfile, index_col=0, encoding='utf-8')

print(atable)
print('-'*50)
print(btable)

atable['chicken'] = '처갓집'
btable['chicken'] = '페리카나'

print(atable)
print(btable)

mylist = []
mylist.append(atable)
mylist.append(btable)
result = pd.concat(objs=mylist, axis=0, ignore_index=True)
print(result)

filename = 'resultchicken.csv'
result.to_csv(filename, encoding='utf-8')
print(filename+ 'saved...')