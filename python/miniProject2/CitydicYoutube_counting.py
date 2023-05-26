# 모듈 및 패키지 임포트
import os
import json
import calendar  # 연도와 월의 일수 계산 모듈
from googleapiclient.discovery import build  # Google API(Youtube API) 사용하기 위한 모듈
from datetime import datetime  # 날짜와 시간 다루기 위한 모듈
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()  # FastAPI 실행

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(
    BASE_DIR, "../secret.json"
)  # secret.json 파일의 JSON 형식으로 된 API키 가져옴
with open(secret_file) as f:
    secret_data = json.load(f)

api_key = secret_data["Youtube_api"]
youtube = build("youtube", "v3", developerKey=api_key)


@app.get("/youtube")  # @app.get 데코레이터 사용하여 /youtube 엔드포인트 생성
async def get_youtube_videos(keywords: str, year: int, month: int):
    if month not in range(1, 13):  # 월이 1~12값이 아니면
        raise ValueError("Month must be between 1 and 12")
    if year not in [2018, 2020, 2022]:  # 2018, 2020, 2022년이여야 함
        raise ValueError("Year must be 2018, 2020, or 2022")

    _, last_day = calendar.monthrange(year, month)  # 해당 월의 첫 번째 요일과 마지막 날짜를 반환
    published_after_date = datetime(year, month, 1)  # year의 해당 month 첫번째 날짜 객체로 생성
    published_before_date = datetime(
        year, month, last_day
    )  # year, month의 lastday를 datetime 객체로 반환

    search_request = youtube.search().list(  # 동영상 검색을 위한 API 요청 생성
        part="snippet",  # 동영상 기본 정보 및 스니펫 요청
        q=keywords,  # 검색할 keywords 지정(keywords로 검색한게 아니라 사용자가 입력하는 검색어(실제 검색어 매개변수))
        order="viewCount",  # 동영상 조회수 기준 정렬
        type="video",  # 동영상만 반환
        publishedAfter=published_after_date.isoformat("T") + "Z",  # 게시 시작일
        publishedBefore=published_before_date.isoformat("T") + "Z",  # 게시 종료일
        maxResults=10,  # 최대 50개 결과 반환
    )

    search_response = search_request.execute()  # 검색 요청 실행한 것 => search_respons에 저장
    result = []  # 리스트 초기화

    for item in search_response["items"]:  # 순회하면서 각 동영상에 대한 정보 가져오기
        video_id = item["id"]["videoId"]  # 각 동영상의 고유한 videoId 추출
        video_request = youtube.videos().list(
            part="snippet,statistics", id=video_id
        )  # 추가정보 요청, 스니펫&통계 정보 요청
        video_response = video_request.execute()
        video_info = video_response["items"][0]
        result.append(
            {
                "Title": video_info["snippet"]["title"],  # 동영상 제목
                "View Count": video_info["statistics"]["viewCount"],  # 동영상 조회수
                "Published At": video_info["snippet"]["publishedAt"],  # 동영상 게시일
                "Tags": video_info["snippet"]["tags"]  # 동영상 태그 수
                if "tags" in video_info["snippet"]  # 태그가 없으면
                else "No tags.",  # No tags
            }
        )
    return result  # result 리스트를 반환하여 API 엔드포인트의 응답으로 전달


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
collection = db["collection2"] #찾아오는 데이터


@app.get("/find")
async def find_videos(year: int, keyword: str):
    months = range(1, 13)  # 1월부터 12월까지의 월

    word_count = {}
    for m in months:
        word_count[m] = 0

        # 월별로 동영상 가져오기
        youtube_videos = await get_youtube_videos(keyword, year, m)

        documents = collection.find({"도시명": ""})

        for document in documents:
            word_count[m] += document.get(str(m), 0)

        titles = [video["Title"] for video in youtube_videos]
        tags = [
            video["Tags"] if video["Tags"] != "No tags." else []
            for video in youtube_videos
        ]

        for title, tag_list in zip(titles, tags):
            title_word_count = title.count(keyword)
            tag_word_count = sum(tag.count(keyword) for tag in tag_list)
            word_count[m] += title_word_count + tag_word_count

    result = {"word_count": {}}

    for m in months:
        result["word_count"][f"{m}월"] = word_count[m]

    # 월별 Word Count를 출력하는 부분
    print("Word Count:")
    for m in months:
        print(f"도시명: {m}월: {word_count[m]}개")

    return result

