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

from apiclient.discovery import build

word = ""

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../../secret.json')

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
