import os
import json
from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

app = FastAPI()  # FastAPI 애플리케이션 객체 생성

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# 현재 스크립트 파일의 상위 디렉토리 경로를 설정

secret_file = os.path.join(BASE_DIR, "../secret.json")
# 상위 디렉토리의 secret.json 파일 경로를 설정

with open(secret_file) as f:
    secrets = json.loads(f.read())
    # secret.json 파일을 읽고 JSON 데이터를 파싱하여 secrets 변수에 저장

HOSTNAME = secrets.get("ATLAS_Hostname")
# secrets 딕셔너리에서 ATLAS_Hostname 키의 값을 가져와 HOSTNAME 변수에 저장

USERNAME = secrets.get("ATLAS_Username")
# secrets 딕셔너리에서 ATLAS_Username 키의 값을 가져와 USERNAME 변수에 저장

PASSWORD = secrets.get("ATLAS_Password")
# secrets 딕셔너리에서 ATLAS_Password 키의 값을 가져와 PASSWORD 변수에 저장

client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
# MongoClient를 사용하여 MongoDB 클라이언트를 생성
# MongoDB 서버에 연결하기 위한 URI를 설정하고, 인증 정보를 포함시킵니다

print("Connected to Mongodb....")
# MongoDB에 연결되었다는 메시지를 출력

db = client["miniProject2"]
# "miniProject2" 데이터베이스에 연결하기 위한 db 변수를 설정

collection = db["collection1"]
# "collection1" 컬렉션에 연결하기 위한 collection 변수를 설정

@app.get("/collection1")
def get_documents():
    documents = collection.find()
    # "collection1" 컬렉션에서 문서를 조회하여 documents 변수에 저장

    result = []
    for document in documents:
        document["_id"] = str(document["_id"])
        # 각 문서의 "_id" 필드 값을 문자열로 변환
        
        result.append(document)
        # 변환된 문서를 result 리스트에 추가

    return result
    # 결과 리스트를 반환

    
