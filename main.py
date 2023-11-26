from fastapi import FastAPI, Response, Path, HTTPException, Body
from typing import List
from resources.resource import UsersResource, User
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

@app.post("/api/users/", response_model=User)
async def create_user(user: User = Body(...)):
    return users_resource.create_user(user)

@app.put("/api/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User = Body(...)):
    return users_resource.update_user(user_id, user)

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    users_resource.delete_user(user_id)
    return {"message": f"User with id {user_id} deleted"}

@app.post("/api/users/login")
async def login_user():
    return {"message": "User logged in"}

@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: int = Path(..., description="The ID of the user to retrieve")):
    return users_resource.get_user(user_id)

@app.get("/api/users/{user_id}/profile")
async def get_user_profile(user_id: int):
    return users_resource.get_user_profile(user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
