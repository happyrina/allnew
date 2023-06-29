#폴더 안에 파일 만들때
import os

myfolder = './'
newpath = os.path.join(myfolder, 'work')

try:
    os.mkdir(path=newpath)

    for idx in range(1, 11):
        newfile = os.path.join(newpath, 'somefolder' + str(idx).zfill(2))
        os.mkdir(path=newfile)
except FileExistsError:
    print('Directory exist already...')
print('finished')