from pymongo import MongoClient
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt
import os
import json
from PIL import Image
import numpy as np

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

# 0부터 11까지 데이터 가져오기
data_array = []
for doc in collection.find().limit(12):
    if 'data' in doc:
        data_array.extend(doc['data'])

# 워드클라우드 생성
text = ' '.join(data_array)

# 이미지 파일을 위한 패스 설정
image_path = "arin_1tokyo.png"

# 이미지 파일을 열고 Numpy 배열로 변환
image_mask = np.array(Image.open(image_path))

# WordCloud 객체 생성, mask 파라미터로 이미지를 사용
wordcloud = WordCloud(width=800, height=800,
                      background_color='white', mask=image_mask).generate(text)

# 결과 출력
wordcloud_image = wordcloud.to_image().convert('RGBA')
fig = px.imshow(wordcloud_image)
fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
fig.show()
