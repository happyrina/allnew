import urllib.request
from bs4 import BeautifulSoup
from pandas import DataFrame

url = "https://movie.daum.net/ranking/reservation"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

infos = soup.findAll('div', attrs={'class':'thumb_cont'})

##여기까지만 두고 크롤링이 되는지 확인
# print('-' * 40)
# print(infos)
# print('-' * 40)

#그리고 이게 가능하다면 이 이후에 있는 것들이 가능해서 크롤링이 가능하다는 말!
# no = 0
# result = []
# for info in infos:
#     no += 1
#     mytitle = info.find('a', attrs={'class':'link_txt'})
#     title = mytitle.string
#
#     mygrade = info.find('span', attrs={'class':'txt_grade'})
#     grade = mygrade.string
#
#     mynum = info.find('span', attrs={'class':'txt_num'})
#     num = mynum.string
#
#     myrelease = info.find('span', attrs={'class':'txt_info'})
#     release = myrelease.span.string
#
#     result.append((no, title, grade, num, release))
# print(result)

# print('-' * 40)
#
# mycolumn = ['순위', '제목', '평점', '애매율', '개봉일']
#
# myframe = DataFrame(result, columns=mycolumn)
# newdf = myframe.set_index(keys=['순위'])
# print(newdf)
# print('-' * 40)
#
# filename = 'daumMovie.csv'
# myframe.to_csv(filename, encoding='utf8', index=False)
# print(filename, ' saved...', sep='')
# print('finished')

