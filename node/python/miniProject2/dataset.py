import random
import pymongo
from pymongo import MongoClient
import json
import os
import matplotlib.pyplot as plt
import numpy as np

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
collection = db["dataset"]

# dataset.json 파일을 읽어서 Python 객체로 변환합니다.
with open('dataset.json', 'r') as file:
    data = json.load(file)

# 확인: 데이터가 리스트인지 확인하십시오. 각 항목이 문서로 취급됩니다.
# 데이터가 딕셔너리라면, 리스트로 변환합니다. [data]

# MongoDB의 dataset 컬렉션에 데이터를 추가합니다.
collection.insert_many(data)