import urllib.request

url = 'https://shared-comic.pstatic.net/thumb/webtoon/648419/thumbnail/thumbnail_IMAG10_1421195d-13be-4cde-bcf9-0c78d51c5ea3.jpg'
savename = input('저장할 파일 이름 입력 : ')

result = urllib.request.urlopen(url)

data = result.read()
print('# type(data : ', type(data))

urllib.request.urlretrieve(url, savename)

print(savename + '파일로 저장되었습니다.')
print(savename + 'saved...')
