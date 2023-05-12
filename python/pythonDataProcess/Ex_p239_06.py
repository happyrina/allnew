from pandas import Series
import matplotlib.pyplot as plt

plt.rc('font', family='AppleGothic')

mylist = [30, 20, 40, 30, 60]
myindex = ['강감찬', '김유신', '이순신', '안익태', '윤동주']
myseries = Series(data=mylist, index=myindex)
myseries.plot(kind='bar', rot = 0,
              use_index=True, grid=False, table=False, color=['r', 'g', 'b', 'y', 'm'])

plt.xlabel("학생 이름")
plt.ylabel("점수")
plt.title("학생별 시험 점수")

ratio = 100 * myseries / myseries.sum()
print(ratio)
print('-' * 40)

for idx in range(myseries.size):
    value = str(myseries[idx]) + '건'
    ratioval = '%.1f%%' % (ratio[idx])
    plt.text(x=idx, y=myseries[idx] + 1, s=value, horizontalalignment='center')
    plt.text(x=idx, y=myseries[idx] / 2, s=ratioval, horizontalalignment='center')

meanval = myseries.mean()
print(meanval)
print('-' * 40)

average = '평균 : %d건' % meanval
plt.axhline(y=meanval, color='r', linewidth=1, linestyle='dashed')
plt.text(x=0, y=meanval + 1, s=average, horizontalalignment='center')

filename = 'graph02.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' Saved...')
plt.show()
