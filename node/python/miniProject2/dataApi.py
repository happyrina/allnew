import json
import os
import requests
from pymongo import MongoClient
from fastapi import FastAPI


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

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
collection = db["collection2"]


@app.get("/data")
def get_data():
    url = 'https://apis.data.go.kr/B551177/StatusOfSrvDestinations/getServiceDestinationInfo'
    response = requests.get(url) 

    data = response.json()  # make sure to check that the response actually contains JSON data

    if "item" in data:
        for item in data["item"]:
            existing_document = collection.find_one(
                {"상대공항코드": item['airport_code']})
            if existing_document is None:
                collection.insert_one(item)

    return {"message": "Data inserted into MongoDB."}

