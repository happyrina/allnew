import os
import json
import pandas as pd
from fastapi import FastAPI
from pymongo import MongoClient

# 기본 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))

# 비밀 파일 로드
secret_file = os.path.join(BASE_DIR, "../secret.json")

# FastAPI 앱 생성
app = FastAPI()

# 비밀 정보를 비밀 파일에서 읽어오기
with open(secret_file) as f:
    secrets = json.loads(f.read())

# 비밀 정보를 가져오는 함수
def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg

# MongoDB 연결 정보 가져오기
HOSTNAME = get_secret("ATLAS_Hostname")
USERNAME = get_secret("ATLAS_Username")
PASSWORD = get_secret("ATLAS_Password")

# MongoDB에 연결
client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
print("Mongodb에 연결되었습니다....")

# 데이터베이스 선택
db = client["miniProject2"]

# 컬렉션 삭제 (이미 존재한다면)
db.drop_collection("collection1")

# 컬렉션 생성
collection = db["collection1"]

# JSON 파일에서 데이터 읽어오기
with open("2022.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 데이터를 DataFrame으로 변환
df = pd.DataFrame(data)

# DataFrame에서 필요한 부분 선택하고 열 이름 변경
df = df.iloc[2:12]
df.columns = ["노선", "상대공항", "운항(편)", "여객(명)", "화물(톤)"]

# DataFrame의 인덱스 초기화
df = df.reset_index(drop=True)

# 상위 10개의 행 선택
df_top10 = df.head(10)

# 선택된 행들을 MongoDB 컬렉션에 삽입
for _, row in df_top10.iterrows():
    collection.insert_one(row.to_dict())

print("데이터가 MongoDB에 삽입되었습니다.")

# 컬렉션에서 모든 문서들을 가져와서 출력
documents = collection.find()
for document in documents:
    print(document)
