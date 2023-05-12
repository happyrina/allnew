import pandas as pd

filename = 'data02.csv'
df = pd.read_csv(filename, header=None, names=['이름', '학년', '국어', '영어', '수학'], index_col=0)
df.loc[['강호민'], ['영어']] = 40
df.loc[['박영희'], ['국어']] = 30
df.reset_index(inplace=True)
print(df[['이름', '학년', '국어', '영어', '수학']].to_string(index=False))



