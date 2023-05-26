# 모듈 및 패키지 임포트
import os
import json
import calendar  # 연도와 월의 일수 계산 모듈
# Google API(Youtube API) 사용하기 위한 모듈
from googleapiclient.discovery import build
from datetime import datetime  # 날짜와 시간 다루기 위한 모듈
from fastapi import FastAPI
from pymongo import MongoClient
import requests
from bson import ObjectId
from urllib.parse import quote

app = FastAPI()

# secret.json 파일에서 API 키를 가져옵니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, "../secret.json")

with open(secret_file) as f:
    secrets = json.load(f)

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
db = client["miniProject2"]
collection = db["2018youtube"]

db = client["miniProject2"]
collection = db["2018count"]  # 찾아오는 데이터

@app.get("/find")
async def find_videos(year: int, keyword: str):
    months = range(1, 13)  # 1월부터 12월까지의 월
    years = [2018, 2020, 2022, 2023]  # 2018년부터 2023년까지의 연도
    city_names = ['도쿄', '오사카', '후쿠오카']  # 검색하려는 도시 리스트

    # 연도별 월별 도시별 키워드 카운트를 저장할 딕셔너리
    count_dict = {year: {month: {city: 0 for city in city_names}
                         for month in months} for year in years}

    for year in years:
        for month in months:
            if year == 2023 and month > 3:  # 2023년은 3월까지만 데이터가 있다고 하셨으므로
                break
            youtube_videos = await get_youtube_videos(keyword, year, month)
            titles = [video["Title"] for video in youtube_videos]
            tags = [
                video["Tags"] if video["Tags"] != "No tags." else []
                for video in youtube_videos
            ]
            for city in city_names:
                documents = collection.find({"도시명": city})  # 해당 도시의 모든 문서를 찾음
                for document in documents:
                    # 연도별 월별 도시별 키워드 카운트를 업데이트
                    count_dict[year][month][city] += document.get(
                        str(month), 0)
                for title, tag_list in zip(titles, tags):
                    title_word_count = title.count(keyword)
                    tag_word_count = sum(tag.count(keyword)
                                         for tag in tag_list)
                    count_dict[year][month][city] += title_word_count + \
                        tag_word_count  # 연도별 월별 도시별 키워드 카운트를 업데이트
    return count_dict  # 최종 결과를 반환