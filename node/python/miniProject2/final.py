import os
import matplotlib.pyplot as plt
from pymongo import MongoClient
from starlette.responses import StreamingResponse
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from pymongo import mongo_client
import os.path
import json
import pydantic
from bson.objectid import ObjectId
from typing import Optional

import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


word = ""

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

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


HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

client = mongo_client.MongoClient(
    f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}')
print('Connected to MongoDB....')

db = client['project2']
db.drop_collection("project2")
col = db['imgdata']

developer_Key = secrets['developer_Key']
cx_value = secrets['cx']


@app.get('/insertmongo')
async def insertMongo(cities: Optional[list[str]] = None):
    if cities is None:
        cities = []

    result = {}

    for city in cities:
        service = build("customsearch", "v1",
                        developerKey=developer_Key)

        res = service.cse().list(
            q=city,
            cx=cx_value,
            searchType='image',
            num=10,
            imgType='clipart',
            fileType='png',
            safe='off'
        ).execute()

        if 'items' not in res:
            result[city] = "No result"
        else:
            word_count = {}
            for item in res['items']:
                title = item['title']
                word_list = title.split()
                for word in word_list:
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1

            result[city] = word_count

    return result


app = FastAPI()

# Secret 정보(여기서는 MongoDB 연결 정보)를 담고 있는 파일을 불러옴
BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, "../secret.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg


# MongoDB에 연결
HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")
client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")

db = client["project2"]
collection = db["Alltextcounting"]


@app.get("/pieChart/{year}")
async def create_pieChart(year: int):
    document = collection.find_one({"year": year})

    if document is None:
        raise HTTPException(status_code=404, detail="Year not found")

    results = document["result"]

    # 파이차트 그리기 위한 데이터 준비
    labels = list(results.keys())
    slices = list(results.values())

    # 파이차트 그리기
    plt.rcParams['font.family'] = 'AppleGothic'
    mycolors = ['#2962FF', '#C51162', '#00C853', '#FF6D00', '#D50000',
                '#0091EA', '#AEEA00', '#FFD600', '#795548', '#18FFFF']
    plt.pie(slices, labels=labels, shadow=False, explode=[0.1] * len(slices),
            colors=mycolors, autopct='%1.2f%%', startangle=90, counterclock=False)

    plt.legend(loc='lower right', fontsize='x-small')

    filename = f'pieGraph{year}.png'
    plt.savefig(filename, dpi=400, bbox_inches='tight')
    plt.clf()  # 현재 figure를 클리어해 다음 요청에 영향이 없도록 합니다.

    file_like = open(filename, mode="rb")
    return StreamingResponse(file_like, media_type="image/png")
