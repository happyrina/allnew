import pymongo
from pymongo import MongoClient
import json
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 기본 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

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

db = client["project2"]
collection = db["Alltextcounting"]

# 2018년도 문서, _id 필드는 제외
document = collection.find_one({"year": 2018}, {"_id": 0, "result": 1})


# 워드클라우드 생성
wordcloud = WordCloud(
    width=800, height=800, background_color="white").generate_from_frequencies(document['result'])

text = document.get("result")
# 워드 클라우드 시각화
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
