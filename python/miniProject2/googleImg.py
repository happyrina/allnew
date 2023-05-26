from fastapi import FastAPI
from pymongo import mongo_client
import os.path
import json
import pydantic
from bson.objectid import ObjectId

from apiclient.discovery import build
# from googleapiclient import discovery

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
print('Connected to Mongodb....')

mydb = client['miniProject2']
mycol = mydb['imgdb']


@app.get('/insertmongo')
async def insertMongo():

    service = build("customsearch", "v1",
                    developerKey="")

    res = service.cse().list(
        q='일본',
        cx='',
        searchType='image',
        num=10,
        imgType='clipart',
        fileType='png',
        safe='off'
    ).execute()
    id = 1
    if not 'items' in res:
        print('No result !!\nres is: {}').format(res)
    else:
        for item in res['items']:
            print('=================================================')
            print(item['title'])
            print(item['link'])
            imgs = dict(id=item['link'])
            mycol.insert_one(imgs)
            result = mycol.find_one({})
            id += 1
    return result
#return의 인덱스가 맞지 않아서... 결과 값이 하나만 담겼음
