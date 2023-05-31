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
collection = db["Alltextcounting"]

def sort_by_value(item):
    return item[1]

# 원하는 연도만 포함시키기
years_to_plot = [2018, 2020, 2022, 2023]
documents = collection.find({"year": {"$in": years_to_plot}}).sort("year", 1)

# 연도와 키워드 추출
keywords = set()
results_by_year = {}
top3_by_year = {}

for document in documents:
    year = document["year"]
    keywords.update(document["result"].keys())
    results_by_year[year] = document["result"]

    # 각 연도별 상위 3개 키워드 찾기
    sorted_results = sorted(
        document["result"].items(), key=lambda x: x[1], reverse=True)
    top3_by_year[year] = sorted_results[:3]

# 결과를 0으로 초기화 및 업데이트
results_for_plot = {keyword: [0]*len(years_to_plot) for keyword in keywords}
for i, year in enumerate(years_to_plot):
    for keyword in keywords:
        if keyword in results_by_year[year]:
            results_for_plot[keyword][i] = results_by_year[year][keyword]

plt.rcParams['font.family'] = 'AppleGothic'


def generate_random_color():
    return '#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

# x축에 대한 별도의 리스트 생성
x = list(range(len(years_to_plot)))

# 누적 막대 그래프 그리기
bar_width = 0.6
for i, keyword in enumerate(keywords):
    color = generate_random_color()
    if i == 0:
        plt.bar(x, results_for_plot[keyword],
                width=bar_width, color=color, label=keyword)
        last_values = np.array(results_for_plot[keyword])
    else:
        plt.bar(x, results_for_plot[keyword], width=bar_width,
                bottom=last_values, color=color, label=keyword)
        last_values += np.array(results_for_plot[keyword])

# 테이블 생성
table_data = []
for year in years_to_plot:
    row = [year] + ['{} ({})'.format(word, count)
                    for word, count in top3_by_year[year]]
    table_data.append(row)

plt.table(cellText=table_data, colLabels=['Year', 'Top 1', 'Top 2', 'Top 3'], cellLoc='center',
          loc='bottom', bbox=[0.1, -0.9, 0.8, 0.6])
plt.subplots_adjust(left=0.1, bottom=0.3)
plt.xlabel('Year')
plt.ylabel('Result')
plt.title('18, 20, 22, 23 전체 언급량 비교')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
# x축 레이블 설정
plt.xticks(x, years_to_plot)
filename = 'alldataGraph.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' Saved...')
plt.show()
