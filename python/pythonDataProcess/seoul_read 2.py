import pandas as pd

filename = 'seoul.csv'
df = pd.read_csv(filename)
print(df)

result =df.loc[(df['시군구'] == ' 서울특별시 강남구 신사동')]
print(result)

result =df.loc[(df['시군구'] == '서울특별시 강남구 신사동') & (df['단지명'] =='삼지')]
print(result)

newdf = df.set_index(keys=['도로명'])
print(newdf)

result = newdf.loc['동일로']
# result =df.loc[(df['도로명'] == ' 언주로 ')] 이렇게 하면 안 나옴... 오류뜸 왜?
print(result)

count = result.size
# count = result.count()
#count = newdf.loc['동일로'].count() 이렇게 나오면 newdf의 모든 데이터 프레임의 정보가 다 나옴
print(count)