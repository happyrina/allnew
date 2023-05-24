import os  # os 모듈은 운영 체제와 상호작용하기 위한 수단을 제공합니다.
import json  # json 모듈은 JSON 데이터를 다루기 위해 사용됩니다.
import calendar  # calendar 모듈은 달력 관련 기능을 제공합니다.
# googleapiclient.discovery의 build 함수는 Google API와 통신하기 위한 서비스 객체를 생성합니다.
from googleapiclient.discovery import build
# datetime 모듈의 datetime 클래스는 날짜와 시간을 함께 처리할 수 있게 합니다.
from datetime import datetime
# FastAPI는 modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints를 생성하는데 사용됩니다.
from fastapi import FastAPI

# 현재 스크립트의 부모 디렉토리의 경로를 얻습니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# secret.json 파일의 경로를 구성합니다.
secret_file = os.path.join(BASE_DIR, "../secret.json")
with open(secret_file) as f:  # secret.json 파일을 읽기 모드로 엽니다.
    secret_data = json.load(f)  # JSON 데이터를 파이썬 객체로 변환합니다.

api_key = secret_data["Youtube_api"]  # JSON 데이터로부터 YouTube API 키를 가져옵니다.
# YouTube API v3 서비스 객체를 생성합니다.
youtube = build("youtube", "v3", developerKey=api_key)

app = FastAPI()  # FastAPI 인스턴스를 생성합니다.


@app.get("/youtube")  # "/youtube" 경로로 GET 요청이 들어오면 아래의 함수를 실행합니다.
async def get_youtube_videos(keywords: str, year: int, month: int):
    if month not in range(1, 13):  # 월이 1 ~ 12 사이가 아니라면 예외를 발생시킵니다.
        raise ValueError("Month must be between 1 and 12")
    # 연도가 2018, 2020, 2022 중 하나가 아니라면 예외를 발생시킵니다.
    if year not in [2018, 2020, 2022]:
        raise ValueError("Year must be 2018, 2020, or 2022")

    _, last_day = calendar.monthrange(year, month)  # 해당 월의 마지막 날을 얻습니다.
    # 해당 월의 첫 날을 datetime 객체로 생성합니다.
    published_after_date = datetime(year, month, 1)
    # 해당 월의 마지막 날을 datetime 객체로 생성합니다.
    published_before_date = datetime(year, month, last_day)

    # YouTube 검색 요청을 구성합니다.
    search_request = youtube.search().list(
        part="snippet",
        q=keywords,
        order="viewCount",  # 반환되는 동영상이 조회수에 따라 정렬됩니다.
        type="video",  # 검색 타입을 "video"로 설정합니다.
        # 이 날짜 이후에 게시된 비디오만 검색합니다.
        publishedAfter=published_after_date.isoformat("T") + "Z",
        # 이 날짜 이전에 게시된 비디오만 검색합니다.
        publishedBefore=published_before_date.isoformat("T") + "Z",
        maxResults=20,  # 최대 20개의 결과를 반환하도록 설정합니다.
    )

    search_response = search_request.execute()  # 검색 요청을 실행하고 결과를 받아옵니다.
    result = []  # 반환할 비디오 정보를 담을 리스트를 초기화합니다.

    for item in search_response["items"]:  # 각 검색 결과에 대해 반복합니다.
        video_id = item["id"]["videoId"]  # 동영상의 ID를 얻습니다.
        # 해당 동영상의 세부 정보를 요청합니다.
        video_request = youtube.videos().list(part="snippet,statistics", id=video_id)
        video_response = video_request.execute()  # 동영상 정보 요청을 실행하고 결과를 받아옵니다.
        video_info = video_response["items"][0]  # 동영상 정보를 변수에 저장합니다.
        # 동영상의 제목, 조회수, 게시 날짜, 태그를 딕셔너리로 만들어 result 리스트에 추가합니다.
        result.append(
            {
                "Title": video_info["snippet"]["title"],
                "View Count": video_info["statistics"]["viewCount"],
                "Published At": video_info["snippet"]["publishedAt"],
                "Tags": video_info["snippet"]["tags"]
                if "tags" in video_info["snippet"]
                else "No tags.",
            }
        )

    return result  # 동영상 정보를 담은 리스트를 반환합니다.

# python -m uvicorn project1:app --host 0.0.0.0 --port 3000 --reload
