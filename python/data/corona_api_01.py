import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from fastapi import FastAPI
import os.path

# secret json import
BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg


app = FastAPI()


@app.get('/')  # 내가 url주소를 요청하는 root 데이터에서.....
async def healthCheck():
    return "OK"


@app.get('/hello')
async def Hello():
    return "Hello World~!!!"


@app.get('/getdata')
async def getData():
    url = 'https://apis.data.go.kr/1352000/ODMS_COVID_02/callCovid02Api'

    # 공공데이터에 나온 연도로 맞춰주려고 strftime함, 대소문자 가림
    # -timedelta 실행하면 어제 날짜가 나옴
    today = (datetime.today() - timedelta(1)).strftime("%Y%m%d")
    print(today)

    params = '?serviceKey=' + get_secret("data_apiKey")
    params += '&pageNo=1'
    params += '&num0fRows=500'
    params += '&apiType=JSON'
    params += '&status_dt=' + str(today)

    url += params
    print(url)

    # 상단에 모듈에 웹사이트 모듈이 없음, 근데 requests 모듈만 사용해도 원격 요청이 가능함, 200으로 옴
    response = requests.get(url)
    print(response)
    print('-' * 50)

    contents = response.text
    print(type(contents))  # 타입을 찍어보면서 어떤 타입으로 오는지 확인하기
    print(contents)
    print('-' * 50)
    # params에 json으로 요청해서 결과값도 json 근데 return값은 str으로 나옴.. 이걸 바꾸려면?

    dict = json.loads(contents)
    print(type(dict))
    print(dict)  # 해당 값은 dictionary로 왔고 json타입임! 실제 원하는 값은 items에,, 여긴 list타입
    print('-' * 50)

    items = dict['items'][0]
    print(type(items))
    print(items)
    print('-' * 50)

    item = ['gPntCnt', 'hPntCnt', 'accExamCnt', 'statusDt']

    validItem = {}
    for _ in item:
        validItem[_] = items[_]
    print(validItem)
    print('-' * 50)

    return validItem
