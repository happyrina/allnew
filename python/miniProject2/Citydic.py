# import csv
# import json
# from pymongo import MongoClient
# from fastapi import FastAPI
# import pandas as pd
# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# secret_file = os.path.join(BASE_DIR, "../secret.json")

# app = FastAPI()
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

# # MongoDB 접속 정보 설정
# client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
# print("Connected to Mongodb....")  # MongoDB 호스트와 포트 설정
# db = client['miniProject2']  # 데이터베이스 선택
# collection = db['mini2']  # 컬렉션 선택

# # CSV 파일을 JSON으로 변환
# csv_file = 'citydic.csv'
# json_data = []
# with open(csv_file, 'r') as file:
#     csv_data = csv.DictReader(file)
#     json_data = [row for row in csv_data]

# # JSON 데이터를 MongoDB에 삽입
# collection.insert_many(json_data)
# print('데이터가 MongoDB에 성공적으로 삽입되었습니다.')
# 위 데이터는 모든 csv파일이 json형태로 mini2 몽고 db에 들어감

# import csv
# import json
# from pymongo import MongoClient
# from fastapi import FastAPI
# import pandas as pd
# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# secret_file = os.path.join(BASE_DIR, "../secret.json")

# app = FastAPI()
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
# print("Connected to Mongodb....")

# db = client["miniProject2"]
# db.drop_collection("collection2")
# collection = db["collection2"]

# # CSV 파일을 JSON으로 변환하면서 중복된 공항 처리
# csv_file = 'citydic.csv'
# json_data = []
# unique_airports = set()
# airport_cities = {}

# with open(csv_file, 'r') as file:
#     csv_data = csv.DictReader(file)
#     for row in csv_data:
#         airport_code = row['공항코드1(IATA)']
#         city = row['도시명']
#         if airport_code not in unique_airports:
#             unique_airports.add(airport_code)
#             airport_cities[airport_code] = [city]
#             json_data.append(row)
#         else:
#             airport_cities[airport_code].append(city)

# # JSON 데이터를 MongoDB에 삽입
# collection.insert_many(json_data)

# # 중복된 공항의 데이터와 해당 공항의 도시 데이터 출력
# for airport_code, cities in airport_cities.items():
#     filter_query = {"공항코드1(IATA)": airport_code}
#     update_query = {"$set": {"도시명": cities}}
#     collection.update_many(filter_query, update_query)

# print("Data inserted into MongoDB.")

# # 중복된 공항과 해당 공항의 도시 데이터 출력
# documents = collection.find()
# for document in documents:
#     print(f"공항: {document['공항코드1(IATA)']}")
#     print(f"도시: {', '.join(document['도시명'])}")
#     print()

# documents = collection.find()
# for document in documents:
#     print(document)
# 해당 코드는 citydic의 공항과 도시 값만 뽑아줌


# import csv
# import json
# from pymongo import MongoClient
# from fastapi import FastAPI
# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
# secret_file = os.path.join(BASE_DIR, "../secret.json")

# app = FastAPI()
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

# # MongoDB connection
# client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}")
# print("Connected to MongoDB....")
# db = client['miniProject2']  # Select database
# collection = db['mini2']  # Select collection

# # CSV file to JSON conversion
# csv_file = 'citydic.csv'
# json_data = []
# with open(csv_file, 'r') as file:
#     csv_data = csv.DictReader(file)
#     for row in csv_data:
#         json_data.append({
#             "공항코드1(IATA)": row["공항코드1(IATA)"],
#             "도시명": row["도시명"]
#         })

# # Insert JSON data into MongoDB
# collection.insert_many(json_data)
# print("Data inserted into MongoDB.")

import os
import json
import pandas as pd
from pymongo import MongoClient

# 데이터 프레임 생성
with open("2022.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df1 = pd.DataFrame(data)
df1 = df1.iloc[2:]
df1.columns = ["노선", "상대공항", "운항(편)", "여객(명)", "화물(톤)"]
df1 = df1.reset_index(drop=True)
df1["상대공항코드"] = df1["상대공항"].apply(lambda x: x.split("(")[1].replace(")", ""))

df2 = pd.read_csv("citydic.csv")

merged_df = pd.merge(df1, df2, left_on="상대공항코드",
                     right_on="공항코드1(IATA)", how="inner")

merged_df["여객(명)"] = pd.to_numeric(merged_df["여객(명)"], errors="coerce")

top10_df = merged_df.nlargest(10, "여객(명)")

# MongoDB 연결
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
db.drop_collection("collection2")
collection = db["collection2"]

# 상대공항과 도시명 추출 후 삽입
for _, row in top10_df.iterrows():
    document = {"상대공항": row["상대공항"], "도시명": row["도시명"]}
    collection.insert_one(document)

# MongoDB에서 데이터 조회 및 출력
documents = collection.find()
for document in documents:
    print(document)
