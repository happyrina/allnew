# defaultdict는 누락된 값을 제공하기 위해 팩토리 함수를 호출하는 딕셔너리 서브 클래스
from operator import itemgetter
from collections import defaultdict
from fastapi import FastAPI  # FastAPI는 빠르고 쉽게 API를 만들 수 있도록 도와주는 웹 프레임워크
from pymongo import MongoClient  # MongoClient는 MongoDB와의 연결을 관리
from datetime import datetime  # datetime은 날짜와 시간을 다루는 라이브러리
from bson.objectid import ObjectId  # ObjectId는 MongoDB의 기본키(_id)의 데이터 타입
from konlpy.tag import Okt  # Okt는 형태소 분석기
import numpy as np  # numpy는 배열, 행렬 등 수치 연산을 위한 라이브러리
import os  # os 모듈은 운영체제와 상호작용하는 데 사용
import json  # json 모듈은 JSON 데이터를 파싱하는 데 사용

# FastAPI 인스턴스 생성
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
db.drop_collection("Textcounting")
collection = db["Textcounting"]

# 형태소 분석기 인스턴스를 생성
okt = Okt()

# JSON 데이터를 로드하는 함수


def load_data_from_json():
    with open("dataset.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


 # 일본과 관련된 단어 리스트
city_name = ['도쿄', '오사카', '후쿠오카']

# 단어를 처리하고, 빈도수를 기록하는 함수


def process_word(word, count_dict):
    if "일본" in word or any(city in word for city in city_name):
        return
    # '일본'이 포함되거나 city_name에 포함된 단어가 있으면 건너뜀
    if word not in count_dict:
        count_dict[word] += 1
    # 단어가 처음 나온 경우, 딕셔너리에 추가하고 빈도수를 1로 설정
    else:
        count_dict[word] += 1


    # 불용어 리스트입니다. 이 단어들은 분석에서 제외
stop_words = np.array(['국', '너', '꼭', '가야', '곳', '알짜', '딩고', '편', '민', '짐', '만난', '멋사', '핑맨', '잠뜰', '잔뜩', '전격', '페스트', '비제', '슴', '에이', '로그', '조디', '바인', '고추', '보지', '섹스', '섹', '드립', '리타', '시', '사', '템', '딥', '쿠', '롯', '청', '바', '무슨', '첫', '뿌셧다', '속', '영', '파', '토',
                       '수닝', '달자', '도티', '제나', '스', '더테일', '의제', '린지', '선바', '퓨디파이', '망', '녀', '부흥부', '흥', '햄햄', '햄구', '구들', '노', '민', '유민', '고', '득', '뿌수', '음', '템', '명', '케', '마', '밍모', '유니', '버셜', '것', '리', '또', '링', '다시', '붐', '쓸모', '바', '수', '분', '위', '쉐도', '킹',
                       '가랏', '몬', '자마자', '수리', '튜버', '행유', '유', '튜버', '쉬', '치치', '부가', '리', '부', '다카', '마츠', '워', '나야', '규', '야시', '타바', '먼봉휴', '의', '타고', '첸', '백시', '왜', '끼', '모든', '마리', '디아', '피글', '데', '일리', '디투', '정도', '두리', '뻑', '변', '안', '전', '알', '퍼', '메', '누', '잭굽', '무조건',
                       '족', '휩', '소프', '때문', '못', '닝', '테린', '일본', '부림', '화', '쿠', '익스', '프레', '듯', '증', '똘킹', '에렌님', '또또', '간다', '트', '트수', '은', '루밍', '짬', '후', '딩셉션', '조랭몬', '에렌디', '잉', '아구', '드뤄', '피유', '루밍쨩', '피버', '량', '이춘', '향', '로', '나미', '티', '온', '레', '거', '를', '특', '깜짝', '봉', '침착',
                       '뱅', '서나', '디', '리랜드', '베지터', '호', '오버', '워치', '트', '듀스', '프듀', '규어', '피', '션', '홀', '키디', '부', '음', '직', '비감', '총', '걸', '샒', '빅', '강', '옥', '제', '화', '급', '머', '에드', '응', '그', '박', '은', '팔자', '재', '걸', '기', '러', '시무', '얘기', '넷', '널', '김혜민', '뉸', '르', '친', '홈', '가기'
                       '끄읏', '겸', '에끼', '간', '요', '송', '보기', '송대', '세', '후', '시미', '추추', '인척', '척', '점', '둥이', '개월', '직접', '토리', '경악', '능', '튜브', '어이', '내', '리카', '호미', '란스', '동안', '짓', '던', '길가', '혐한', '준', '우왕', '왁', '오브', '리그', '챗', '날', '더', '게로', '역시', '이', '어쩐지', '이엠', '윤', '씨방',
                       '가장', '신의', '최강', '삼환', '가몬', '오메', '중', '구', '하나', '앞', '패', '확', '과연', '이로리', '뿌', '때', '걸세', '순', '움', '가득', '만', '다', '이제야', '카', '툰', '하편', '코', '가점', '박후기', '나', '북', '퐝', '초', '다츠'])
arrayStopWords = dict(enumerate(stop_words, 1))  # 처음 key값을 1부터 시작하고 싶어서 1을 추가
print(arrayStopWords)


@app.get("/find")
async def get_youtube_videos(year: int):
    # 분석 가능한 연도와 그 연도의 유효한 월을 정의
    years = [2018, 2020, 2022, 2023]
    months_2023 = range(1, 6) if datetime.now().year == 2023 else range(1, 13)

    if year not in years:
        return {"error": "잘못된 연도입니다."}

    if year == 2023:
        valid_months = months_2023
    else:
        valid_months = range(1, 13)

    data = load_data_from_json()  # 데이터를 로드

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

        # 빈도수가 0보다 큰 단어들만 결과에 포함
        month_count = {word: count for word,
                       count in count_dict.items() if count > 0}
        # 문자열로 변환된 "month"를 키로 사용하여 결과를 저장
        result[str(month)] = month_count

    # 결과를 MongoDB에 저장
    collection.insert_one({"year": year, "result": result})

    return result
###############################################


def get_top10_words(word_count_dict):
    # 단어의 빈도수를 기준으로 내림차순 정렬
    sorted_dict = sorted(word_count_dict.items(),
                         key=itemgetter(1), reverse=True)
    # 상위 10개의 단어와 그 빈도수를 반환
    return dict(sorted_dict[:10])

@app.get("/find/top10")
async def get_youtube_videos(year: int):
    # 분석 가능한 연도와 그 연도의 유효한 월을 정의
    years = [2018, 2020, 2022, 2023]
    months_2023 = range(1, 6) if datetime.now().year == 2023 else range(1, 13)

    if year not in years:
        return {"error": "잘못된 연도입니다."}

    if year == 2023:
        valid_months = months_2023
    else:
        valid_months = range(1, 13)

    data = load_data_from_json()  # 데이터를 로드

    count_dict = defaultdict(int)
    for month in valid_months:
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

    # 빈도수가 0보다 큰 단어들만 결과에 포함
    year_count = {word: count for word,
                  count in count_dict.items() if count > 0}
    # 상위 10개 단어를 추출
    top10_words = get_top10_words(year_count)

    # 결과를 MongoDB에 저장
    collection.insert_one({"year": year, "result": top10_words})

    return top10_words
