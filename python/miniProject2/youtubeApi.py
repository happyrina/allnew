import os
import json
from googleapiclient.discovery import build
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, validator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, "../secret.json")
with open(secret_file) as f:
    secret_data = json.load(f)

api_key = secret_data["Youtube_api"]
youtube = build("youtube", "v3", developerKey=api_key)

app = FastAPI()


@app.get("/youtube")
async def get_youtube_videos(keywords: str, year: int):
    if year not in [2018, 2020, 2022]:
        raise ValueError("Year must be 2018, 2020, or 2022")
    # 지정된 연도가 2018, 2020, 2022 중 하나가 아니라면 ValueError를 발생시킵니다.

    published_after_date = datetime(year, 1, 1)
    published_before_date = datetime(year, 12, 31)
    # 주어진 연도의 시작일과 종료일을 설정합니다.

    search_request = youtube.search().list(
        part="snippet",
        q=keywords,
        order="viewCount",
        type="video",
        publishedAfter=published_after_date.isoformat("T") + "Z",
        publishedBefore=published_before_date.isoformat("T") + "Z",
        maxResults=100,
    )
    # YouTube API를 사용하여 검색 요청을 생성합니다.
    # part는 snippet만 포함하고, keywords에는 입력된 검색어를 사용합니다.
    # order는 조회수(viewCount)를 기준으로 정렬하며, type은 비디오(video)만 검색합니다.
    # publishedAfter와 publishedBefore는 주어진 연도의 시작일과 종료일을 설정합니다.
    # maxResults는 최대 결과 수를 20으로 지정합니다.

    search_response = search_request.execute()
    # 검색 요청을 실행하여 검색 결과를 가져옵니다.

    result = []
    # 결과를 저장할 리스트를 초기화합니다.

    for item in search_response["items"]:
        video_id = item["id"]["videoId"]
        # 검색 결과에서 비디오 ID를 추출합니다.

        video_request = youtube.videos().list(part="snippet,statistics", id=video_id)
        video_response = video_request.execute()
        video_info = video_response["items"][0]
        # 비디오에 대한 추가 정보를 가져옵니다.

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
        # 비디오의 제목, 조회수, 게시일 및 태그 정보를 결과 리스트에 추가합니다.

    return result
    # 최종 결과를 반환합니다.
