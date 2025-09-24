from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import sqlalchemy as db
from sqlalchemy import Table

import string
import random

engine = db.create_engine('mysql+pymysql://root:brp%402004@localhost:3306/employee')
metadata=db.MetaData()
employee_info = Table('employee_info',metadata,autoload_with=engine)
stmt = db.select(employee_info).where(employee_info.columns.salary==30000)

with engine.connect() as conn:
    results = conn.execute(stmt).fetchall()
    for row in results:
        print(row[1])

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
    allow_headers=["*"]
)

class URL(BaseModel):
    url:str

def generate_code(digits=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(digits))
url_mapping={}
domain = "http://127.0.0.1:8000/"

@app.get("/")
def get_root():
    return {"Hello":"World"}

@app.post("/save_url")
def save_url(item:URL):
    if item.url in url_mapping:
        return {"shortened_url":url_mapping[item.url],"all_urls":url_mapping}
    url_mapping[item.url]=domain+generate_code()
    print(url_mapping)
    return {"shortened_url":url_mapping[item.url],"all_urls":url_mapping}

@app.get("/{shortId}")
def render_longURL(shortId:str): 
    original_url=""
    for longurl,shorturl in url_mapping.items():
        if shorturl.endswith(shortId):
            original_url=longurl
        else:
            return {"msg":"URL not found"}
        return RedirectResponse(longurl)




    