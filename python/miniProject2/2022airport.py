import os
import json
import pandas as pd
from fastapi import FastAPI
from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, "../secret.json")

app = FastAPI()
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
print("Connected to Mongodb....")

db = client["miniProject2"]
db.drop_collection("collection1")
collection = db["collection1"]

with open("2022.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)
df = df.iloc[2:12]
df.columns = ["노선", "상대공항", "운항(편)", "여객(명)", "화물(톤)"]
df = df.reset_index(drop=True)

df_top10 = df.head(10)

for _, row in df_top10.iterrows():
    collection.insert_one(row.to_dict())

print("Data inserted into MongoDB.")

documents = collection.find()
for document in documents:
    print(document)