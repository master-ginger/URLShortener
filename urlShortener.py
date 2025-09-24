from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import sqlalchemy as db
from sqlalchemy import Table,insert,select

import string
import random

engine = db.create_engine('mysql+pymysql://root:brp%402004@localhost:3306/demoschema')
metadata=db.MetaData()
url_table = Table('url_mapping',metadata,autoload_with=engine)




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
    code=generate_code()
    stmt = insert(url_table).values(original_url=item.url,short_code=code)
    stmt2 = select(url_table)

    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()
        result = conn.execute(stmt2).fetchall()
        for row in result:
            print(row)
    
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




    