from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime
import requests
import json
import os


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, "../../secret.json")

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
    with open("../dataset.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


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

    count_dict = {year: {month: 0 for month in valid_months}}

    for year_data in data:
        if year_data["Year"] == year:
            for item in year_data["Data"]:
                month = int(item["Published At"][5:7])
                # Use .get() to handle missing key
                city_name = item.get("City")
                if month in valid_months and city_name not in city_names:
                    title_word_count = item["Title"].count(search_keyword)
                    tag_word_count = sum(tag.count(search_keyword)
                                         for tag in item["Tags"])
                    count_dict[year][month] += title_word_count + \
                        tag_word_count

    result = {
        "search_keyword": search_keyword,
        "count_dict": count_dict
    }
    return result
