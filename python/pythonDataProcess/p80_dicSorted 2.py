wordInfo = {'세탁기' : 50, '선풍기' : 30, '청소기' : 40, '냉장고' : 60}

myxticks = sorted(wordInfo, key=wordInfo.get, reverse=True)
print(myxticks)
#값에 의한 정렬 그래서 냉장고가 젤 큼! value값이 큰 것 부터 정렬

revers_key = sorted(wordInfo.keys(), reverse=True)
print(revers_key)

chartdata = sorted(wordInfo.values(), reverse=True)
print(chartdata)