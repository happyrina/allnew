# 
from collections import defaultdict
import re
from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime
import requests
import json
import os.path
import pydantic
from bson.objectid import ObjectId
from typing import Optional
from googleapiclient.discovery import build


pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

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


HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
print("Connected to MongoDB....")

db = client["miniProject2"]
collection = db["datacount"]  # MongoDB에 데이터 넣기


def load_data_from_json():
    with open("dataset.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Rest of your code...


def process_word(word, search_keyword, count_dict):
    if word not in count_dict:
        count_dict[word] = 0
    if search_keyword in word:
        count_dict[word] += 1


@app.get("/find")
async def get_youtube_videos(search_keyword: str, year: int):
    city_names = ['도쿄', '오사카', '후쿠오카']
    years = [2018, 2020, 2022, 2023]
    months_2023 = range(1, 6) if datetime.now().year == 2023 else range(1, 13)

    if year not in years:
        return {"error": "잘못된 연도입니다."}

    if year == 2023:
        valid_months = months_2023
    else:
        valid_months = range(1, 13)

    data = load_data_from_json()

    count_dict = defaultdict(int)

    for year_data in data:
        if year_data["Year"] == year:
            for item in year_data["Data"]:
                month = int(item["Published At"][5:7])
                if month in valid_months:
                    title = item["Title"]
                    tags = item["Tags"]
                    words = re.findall(r'\w+', title + ' '.join(tags))
                    for word in words:
                        process_word(word, search_keyword, count_dict)

    for city_name in city_names:
        if city_name in count_dict:
            del count_dict[city_name]

    result = {
        "search_keyword": search_keyword,
        "count_dict": dict(count_dict)
    }
    return result
