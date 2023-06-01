from fastapi import FastAPI, File, File
from fastapi.responses import FileResponse
from fastapi_pagination import add_pagination, paginate
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os.path
import json

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


HOSTNAME = get_secret("Mysql_Hostname")
PORT = get_secret("Mysql_Port")
USERNAME = get_secret("Mysql_Username")
PASSWORD = get_secret("Mysql_Password")
DBNAME = get_secret("Mysql_DBname")

DB_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}"

Base = declarative_base()


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    data = Column(LargeBinary)


def db_conn():
    engine = create_engine(DB_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


app = FastAPI()

# 이미지 추가 API


@app.post("/upload_image/{name}")
async def upload_image(name: str, img: UploadFile = File(...)):
    session = db_conn()

    binary_data = await img.read()
    image = Image(name=name, data=binary_data)
    session.add(image)
    session.commit()
    session.close()

    return {"result": "Image uploaded and stored successfully"}

# 이미지 검색 API


@app.get("/get_image/{name}")
async def get_image(name: str):
    session = db_conn()

    image_data = session.query(Image).filter(Image.name == name).first()
    session.close()

    if image_data:
        with open(f"{name}.png", "wb") as file:
            file.write(image_data.data)
        return FileResponse(path=f"{name}.png", media_type="image/png")
    else:
        return {"error": "Image not found"}

add_pagination(app)
