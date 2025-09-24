from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React dev server
    allow_methods=["*"],
    allow_headers=["*"]
)

class Profile(BaseModel):
    username:str
    bio:str
    followers:int

profiles={}

@app.get("/")
async def read_root():
    return {"message":"Hellow world"}

@app.post("/profile/")
def create_user(profile:Profile):
    profiles[profile.username]={'username':profile.username,'bio':profile.bio,'followers':profile.followers}
    print(profiles)
    return profiles[profile.username]

@app.get("/profile/{username}")
def get_user(username:str):
    print(username in profiles)
    if username in profiles:
        profile=profiles[username]
        print(profile)
        return profile
    return {'username':username,'bio':'Profile Not Found','followers':'-'}

@app.put("/profile/{username}")
def update_user(username:str,profile:Profile):
    if username in profiles:
        profiles[username]={'username':username,'bio':profile.bio,'followers':profile.followers}
    print(profiles)
    return profiles[username]

@app.delete("/profile/{username}")

def delete_user(username:str):
    if username in profiles:
        del profiles[username]
        return {"msg":"Deleted Successfully"}
    return {"msg":"User not found"}

items={
    "id":1,"name":"Book","Price":350,
    "id":2,"name":"Cake","Price":400
}
@app.get("/items/")
def get_items():
    return items