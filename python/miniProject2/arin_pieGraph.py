import pymongo
from pymongo import MongoClient
import json
import os
import matplotlib.pyplot as plt

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
collection = db["Alltextcounting"]
document = collection.find_one({"year": 2023})

if document is not None:
    results = document["result"]
    print(results)

# 파이차트 그리기 위한 데이터 준비
labels = list(results.keys())
slices = list(results.values())

# # # 파이차트 그리기
plt.rcParams['font.family'] = 'AppleGothic'
mycolors = ['#2962FF', '#C51162', '#00C853', '#FF6D00', '#D50000',
            '#0091EA', '#AEEA00', '#FFD600', '#795548', '#18FFFF']
plt.pie(slices, labels=labels, shadow=False, explode=[0.1] * len(slices),
        colors=mycolors, autopct='%1.2f%%', startangle=90, counterclock=False)

plt.legend(loc='lower right', fontsize='x-small')

filename = 'pieGraph2023.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + 'Saved...')
plt.show()

# pieGraph2018 = collection.find_one({}, {"result": 1, "_id": 0})["result"]
# print(pieGraph2018)
# 데이터를 찾아올땐 find, 집어 넣을땐 insert!
# db는 몽고 db에 내가 만든 db폴더명
# collection은 db폴더 아래에 있는 파일들
# find one을 하더라도 {}전체에서 조건을 주면 값이 나와야함..!
#

# # 모든 문서를 리스트로 변환
# all_results = list(collection.find_one({}, {"result": 1, "_id": 0}))

# # 2번째 'result' 값을 가져옴 (인덱스는 0부터 시작하므로 1로 설정)
# result = all_results[1]["result"]

# # 사전의 값들만 추출하여 리스트로 변환
# slices = list(result.values())
# labels = list(result.keys())

# # autopct에 전달할 함수를 정의


# def autopct_generator(slices):
#     def inner_autopct(pct):
#         total = sum(slices)
#         val = int(round(pct*total/100.0))
#         if pct > 6:
#             return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
#         else:
#             return ''
#     return inner_autopct


# plt.rcParams['font.family'] = 'AppleGothic'
# mycolors = ['#2962FF', 'C51162', '#00C853', '#FF6D00', '#D50000',
#             '#0091EA', '#AEEA00', '#FFD600', '#795548', '#18FFFF']
# plt.pie(slices, labels=labels, shadow=False, explode=[0.1] * len(slices),
#         colors=mycolors, autopct=autopct_generator(slices), startangle=90, counterclock=False)

# filename = 'pieGraph2020.png'
# plt.legend(labels, loc="center left",
#            bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
# plt.savefig(filename, dpi=400, bbox_inches='tight')
# print(filename + ' Saved...')
# plt.show()
