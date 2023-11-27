from fastapi import FastAPI, Response, Path, HTTPException, Body
from typing import List
from resources.resource import UsersResource, User, Insert
from database.database import Database

# Database connection
connection_string = ""
database = Database(connection_string)

app = FastAPI()

users_resource = UsersResource(database)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/docs")
async def get_api_docs():
    return {"message": "API documentation available at /docs"}

@app.get("/api/users", response_model=List[User])
async def get_users():
    return users_resource.get_all_users()

@app.post("/api/users/", response_model=Insert)
async def create_user(user_data: Insert = Body(...)):
    return users_resource.create_user(user_data)

@app.put("/api/users/{username}", response_model=dict)
async def update_user(username: str, user: Insert = Body(...)):
    return users_resource.update_user(username, user)

@app.delete("/api/users/{username}")
async def delete_user(username: str):
    return users_resource.delete_user(username)

@app.post("/api/users/login")
async def login_user():
    return {"message": "User logged in"}

@app.get("/api/users/{username}", response_model=User)
async def get_user(username: str):
    return users_resource.get_user(username)

@app.get("/api/users/{username}/profile")
async def get_user_profile(username: str):
    return users_resource.get_user_profile(username)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
