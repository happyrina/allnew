import pandas as pd
from fastapi import FastAPI
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId
import os.path
import json

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
mycol = mydb['2018count']

@app.get("/userupdate")
async def userupdate(id=None, name=None):
    if ("한글국가명" and "연도") is None:
        return "id, name을 입력하세요"
    else:
        user = mycol.find_one({"id": id})
        if user:
            filter = {'id': id}
            data = {"$set": {'name': name}}
            mycol.update_one(filter, data)
            result = mycol.find_one({"id": id})
            return result
        else:
            return f"id={id} 데이터가 존재하지 않습니다."

# 데이터를 읽어옵니다.
df = pd.read_csv('arin.csv')

# 한글 국가명을 입력합니다.
country_name = input("한글로 국가명을 입력해 주세요: ")

# 여행 키워드를 입력합니다.
travel_keyword = input("여행 키워드를 입력해 주세요: ")

# 국가명과 여행 키워드가 모두 포함된 행들을 선택합니다.
selected_rows = df[df['한글국가명'].str.contains(
    country_name) & df['여행'].str.contains(travel_keyword)]

# 해당 행들에서 도시명이 얼마나 자주 등장하는지를 계산합니다.
city_counts = selected_rows['도시명'].value_counts()

print(city_counts)
