from fastapi import FastAPI
from pymongo import MongoClient
import requests
import json
import os

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


@app.get("/find")
async def find_videos(year: int):
    months = range(1, 13)  # 1월부터 12월까지의 월
    years = [2018, 2020, 2022, 2023]  # 2018, 2020, 2022, 2023년까지의 연도
    city_names = ['도쿄', '오사카', '후쿠오카']  # 검색하려는 도시 리스트

    # 연도별 월별 도시별 키워드 카운트를 저장할 딕셔너리
    count_dict = {year: {month: {city: 0 for city in city_names}
                         for month in months} for year in years}

    file_names = ["arin_2018.json", "arin_2020.json",
                  "arin_2022.json", "arin_2023.json"]

    for year, file_name in zip(years, file_names):
        for month in months:
            if year == 2023 and month > 3:  # 2023년은 3월까지만 데이터
                break

            # JSON 파일에서 데이터를 가져와서 youtube_videos 변수에 저장
            with open(file_name, "r") as file:
                youtube_videos = json.load(file)

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

# 33333


# api_key = secrets["Youtube_api"]
# youtube = build("youtube", "v3", developerKey=api_key)

# result = []

# @app.get("/youtube")
# async def get_youtube_videos(keywords: str, year: int):
#     global result

#     if year not in [2018, 2020, 2022, 2023]:
#         raise ValueError("Year must be 2018, 2020, 2022 or 2023")

#     result.clear()

#     encoded_keywords = quote(keywords) #한글 키워드를 URL 인코딩

#     for month in range(1, 13):
#         _, last_day = calendar.monthrange(year, month)
#         published_after_date = datetime(year, month, 1)
#         published_before_date = datetime(year, month, last_day)

    # month = range(1, 13)
    # if month not in range(1, 13):  # 월이 1~12값이 아니면
    #     raise ValueError("Month must be between 1 and 12")
    # if year not in [2018, 2020, 2022, 2023]:  # 2018, 2020, 2022년이여야 함
    #     raise ValueError("Year must be 2018, 2020, 2022 or 2023")

    # _, last_day = calendar.monthrange(year, month)  # 해당 월의 첫 번째 요일과 마지막 날짜를 반환
    # # year의 해당 month 첫번째 날짜 객체로 생성
    # published_after_date = datetime(year, month, 1)
    # published_before_date = datetime(
    #     year, month, last_day
    # )  # year, month의 lastday를 datetime 객체로 반환

    # search_request = youtube.search().list(  # 동영상 검색을 위한 API 요청 생성
    #     part="snippet",  # 동영상 기본 정보 및 스니펫 요청
    #     # 검색할 keywords 지정(keywords로 검색한게 아니라 사용자가 입력하는 검색어(실제 검색어 매개변수))
    #     q=keywords,
    #     order="viewCount",  # 동영상 조회수 기준 정렬
    #     type="video",  # 동영상만 반환
    #     publishedAfter=published_after_date.isoformat("T") + "Z",  # 게시 시작일
    #     publishedBefore=published_before_date.isoformat("T") + "Z",  # 게시 종료일
    #     maxResults=50,  # 최대 50개 결과 반환
    # )

    # search_response = search_request.execute()  # 검색 요청 실행한 것 => search_respons에 저장

    # for item in search_response["items"]:  # 순회하면서 각 동영상에 대한 정보 가져오기
    #     video_id = item["id"]["videoId"]  # 각 동영상의 고유한 videoId 추출
    #     video_request = youtube.videos().list(
    #         part="snippet,statistics", id=video_id
    #     )  # 추가정보 요청, 스니펫&통계 정보 요청
    #     video_response = video_request.execute()
    #     video_info = video_response["items"][0]

    #     tags = video_info["snippet"]["tags"] if "tags" in video_info["snippet"] else []
    #     video_info["snippet"]["tags"] = tags

    #     result.append({
    #         "_id": str(ObjectId()),
    #         "Title": video_info["snippet"]["title"],
    #         "View Count": video_info["statistics"]["viewCount"],
    #         "Published At": video_info["snippet"]["publishedAt"],
    #         "Tags": tags
    #     })

# client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
# db = client["miniProject2"]
# collection = db["2018youtube"]

    #     result.append(
    #         {
    #             "Title": video_info["snippet"]["title"],  # 동영상 제목
    #             "View Count": video_info["statistics"]["viewCount"],  # 동영상 조회수
    #             # 동영상 게시일
    #             "Published At": video_info["snippet"]["publishedAt"],
    #             "Tags": video_info["snippet"]["tags"]  # 동영상 태그 수
    #             if "tags" in video_info["snippet"]  # 태그가 없으면
    #             else "No tags.",  # No tags
    #         }
    #     )
    # return result  # result 리스트를 반환하여 API 엔드포인트의 응답으로 전달


# @app.get("/find")
# async def find_videos(year: int, keyword: str):
#     months = range(1, 13)  # 1월부터 12월까지의 월

#     word_count = {}
#     for m in months:
#         word_count[m] = 0

#         # 월별로 동영상 가져오기
#         youtube_videos = await get_youtube_videos(keyword, year, m)

#         # '도시명'을 일본의 도시로 설정하고, 해당하는 문서를 찾아옵니다.
#         # 예를 들어, 여기서 '도시명'이 '도쿄'라면 도쿄에 대한 정보를 찾아옵니다.
#         # 실제로는 여러 도시에 대해 반복하며 검색하고자 하는 경우, 이 부분을 반복문으로 감싸면 됩니다.

#         city_name = ['도쿄', '오사카',  ]
#         documents = collection.find({"도시명": city_name})

#         for document in documents:
#             word_count[m] += document.get(str(m), 0)

#         titles = [video["Title"] for video in youtube_videos]
#         tags = [
#             video["Tags"] if video["Tags"] != "No tags." else []
#             for video in youtube_videos
#         ]

#         for title, tag_list in zip(titles, tags):
#             title_word_count = title.count(keyword)
#             tag_word_count = sum(tag.count(keyword) for tag in tag_list)
#             word_count[m] += title_word_count + tag_word_count

#     result = {"word_count": {}}

#     for m in months:
#         result["word_count"][f"{m}월"] = word_count[m]

#     # 월별 Word Count를 출력하는 부분
#     print("Word Count:")
#     for m in months:
#         print(f"{city_name}: {m}월: {word_count[m]}개")

#     return result
########################################################################################
