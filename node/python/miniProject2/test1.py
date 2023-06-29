# from collections import defaultdict
# import re
# from fastapi import FastAPI
# from pymongo import MongoClient
# from datetime import datetime
# import requests
# import json
# import os.path
# import pydantic
# from bson.objectid import ObjectId
# from typing import Optional
# from googleapiclient.discovery import build


# pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

# app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# secret_file = os.path.join(BASE_DIR, "../secret.json")

# with open(secret_file) as f:
#     secrets = json.loads(f.read())


# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets[setting]
#     except KeyError:
#         errorMsg = "Set the {} environment variable.".format(setting)
#         return errorMsg


# HOSTNAME = get_secret("ATLAS_Hostname")
# USERNAME = get_secret("ATLAS_Username")
# PASSWORD = get_secret("ATLAS_Password")

# client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
# print("Connected to MongoDB....")

# db = client["miniProject2"]
# collection = db["datacount"]  # MongoDB에 데이터 넣기


# def load_data_from_json():
#     with open("dataset.json", "r", encoding="utf-8") as file:
#         data = json.load(file)
#     return data

# # Rest of your code...


# def process_word(word, search_keyword, count_dict):
#     if word not in count_dict:
#         count_dict[word] += 1
#     if search_keyword in word:
#         count_dict[word] = 0


# @app.get("/find")
# async def get_youtube_videos(search_keyword: str, year: int):
#     city_names = ['도쿄', '오사카', '후쿠오카']
#     years = [2018, 2020, 2022, 2023]
#     months_2023 = range(1, 6) if datetime.now().year == 2023 else range(1, 13)

#     if year not in years:
#         return {"error": "잘못된 연도입니다."}

#     if year == 2023:
#         valid_months = months_2023
#     else:
#         valid_months = range(1, 13)

#     data = load_data_from_json()

#     count_dict = defaultdict(int)

#     for year_data in data:
#         if year_data["Year"] == year:
#             for item in year_data["Data"]:
#                 month = int(item["Published At"][5:7])
#                 if month in valid_months:
#                     title = item["Title"]
#                     tags = item["Tags"]
#                     words = re.findall(r'\w+', title + ' '.join(tags))
#                     for word in words:
#                         process_word(word, search_keyword, count_dict)

#     for city_name in city_names:
#         if city_name in count_dict:
#             del count_dict[city_name]

#     result = {
#         "search_keyword": search_keyword,
#         "count_dict": dict(count_dict)
#     }
#     return result

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

from konlpy.tag import Okt
from nltk.corpus import stopwords

import numpy as np


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

db = client["project2"]
# db.drop_collection("Textcounting")
collection = db["Textcounting"]  # MongoDB에 데이터 넣기

okt = Okt()


def load_data_from_json():
    with open("dataset.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


city_name = ['도쿄', '오사카', '후쿠오카']


def process_word(word, count_dict):
    if "일본" in word or any(city in word for city in city_name):
        return
    if word not in count_dict:
        count_dict[word] += 1

    # if search_keyword in word:
    #     count_dict[word] = 0
    # for city_name in city_names:
    #     if city_name in word:
    #         count_dict[word] = 0


# 해당 부분 실행시 일단 2018년도는 불용어 처리 완료되었음! 2023까지 완료!
stop_words = np.array(['국', '너', '꼭', '가야', '곳', '알짜', '딩고', '편', '민', '짐', '만난', '멋사', '핑맨', '잠뜰', '잔뜩', '전격', '페스트', '비제', '슴', '에이', '로그', '조디', '바인', '고추', '보지', '섹스', '섹', '드립', '리타', '시', '사', '템', '딥', '쿠', '롯', '청', '바', '무슨', '첫', '뿌셧다', '속', '영', '파', '토',
                      '수닝', '달자', '도티', '제나', '스', '더테일', '의제', '린지', '선바', '퓨디파이', '망', '녀', '부흥부', '흥', '햄햄', '햄구', '구들', '노', '민', '유민', '고', '득', '뿌수', '음', '템', '명', '케', '마', '밍모', '유니', '버셜', '것', '리', '또', '링', '다시', '붐', '쓸모', '바', '수', '분', '위', '쉐도', '킹',
                            '가랏', '몬', '자마자', '수리', '튜버', '행유', '유', '튜버', '쉬', '치치', '부가', '리', '부', '다카', '마츠', '워', '나야', '규', '야시', '타바', '먼봉휴', '의', '타고', '첸', '백시', '왜', '끼', '모든', '마리', '디아', '피글', '데', '일리', '디투', '정도', '두리', '뻑', '변', '안', '전', '알', '퍼', '메', '누', '잭굽', '무조건',
                            '족', '휩', '소프', '때문', '못', '닝', '테린', '일본', '부림', '화', '쿠', '익스', '프레', '듯', '증', '똘킹', '에렌님', '또또', '간다', '트', '트수', '은', '루밍', '짬', '후', '딩셉션', '조랭몬', '에렌디', '잉', '아구', '드뤄', '피유', '루밍쨩', '피버', '량', '이춘', '향', '로', '나미', '티', '온', '레', '거', '를', '특', '깜짝', '봉', '침착',
                            '뱅', '서나', '디', '리랜드', '베지터', '호', '오버', '워치', '트', '듀스', '프듀', '규어', '피', '션', '홀', '키디', '부', '음', '직', '비감', '총', '걸', '샒', '빅', '강', '옥', '제', '화', '급', '머', '에드', '응', '그', '박', '은', '팔자', '재', '걸', '기', '러', '시무', '얘기', '넷', '널', '김혜민', '뉸', '르', '친', '홈', '가기'
                            '끄읏', '겸', '에끼', '간', '요', '송', '송대', '세', '후', '시미', '추추', '인척', '척', '점', '둥이', '개월', '직접', '토리', '경악', '능', '튜브', '어이', '내', '리카', '호미', '란스', '동안', '짓', '던', '길가', '혐한', '준', '우왕', '왁', '오브', '리그', '챗', '날', '더', '게로', '역시', '이', '어쩐지', '이엠', '윤', '씨방',
                            '가장', '신의', '최강', '삼환', '가몬', '오메', '중', '구', '하나', '앞', '패', '확', '과연', '이로리', '뿌', '때', '걸세', '순', '움', '가득', '만', '다', '이제야', '카', '툰', '하편', '코', '가점', '박후기', '나', '북', '퐝', '초', '다츠'])
arrayStopWords = dict(enumerate(stop_words, 1))  # 처음 key값을 1부터 시작하고 싶어서 1을 추가
print(arrayStopWords)
# json 파일로 마지막에 저장하기, dic

@app.get("/find")
async def get_youtube_videos(year: int):
    years = [2018, 2020, 2022, 2023]
    months_2023 = range(1, 6) if datetime.now().year == 2023 else range(1, 13)

    if year not in years:
        return {"error": "잘못된 연도입니다."}

    if year == 2023:
        valid_months = months_2023
    else:
        valid_months = range(1, 13)

    data = load_data_from_json()

    result = {}
    for month in valid_months:
        count_dict = defaultdict(int)
        for year_data in data:
            if year_data["Year"] == year:
                for item in year_data["Data"]:
                    item_month = int(item["Published At"][5:7])
                    if item_month == month:
                        title = item["Title"]
                        tags = item["Tags"]
                        text = title + ' '.join(tags)
                        nouns = okt.nouns(text)
                        for noun in nouns:
                            if noun not in stop_words:
                                process_word(noun, count_dict)

        month_count = {word: count for word,
                       count in count_dict.items() if count > 0}
        result[str(month)] = month_count  # "month"를 문자열로 변환하여 사용합니다.
    
    collection.insert_one({"year": year, "result": result})

    return result
# @app.get("/find")
# async def get_youtube_videos(year: int):
#     years = [2018, 2020, 2022, 2023]
#     months_2023 = range(1, 6) if datetime.now().year == 2023 else range(1, 13)

#     if year not in years:
#         return {"error": "잘못된 연도입니다."}

#     if year == 2023:
#         valid_months = months_2023
#     else:
#         valid_months = range(1, 13)

#     data = load_data_from_json()

#     result = {}
#     for month in valid_months:
#         count_dict = defaultdict(int)
#         for year_data in data:
#             if year_data["Year"] == year:
#                 for item in year_data["Data"]:
#                     item_month = int(item["Published At"][5:7])
#                     if item_month == month:
#                         title = item["Title"]
#                         tags = item["Tags"]
#                         text = title + ' '.join(tags)
#                         nouns = okt.nouns(text)
#                         for noun in nouns:
#                             if noun not in stop_words:
#                                 process_word(noun, count_dict)

#         month_count = {word: count for word,
#                        count in count_dict.items() if count > 0}
#         result[month] = month_count

#     collection.insert_one({"year": year, "result": result})

#     return result
