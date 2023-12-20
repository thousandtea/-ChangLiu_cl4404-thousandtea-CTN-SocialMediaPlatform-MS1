from fastapi import FastAPI, Response, Path, HTTPException, Body
from fastapi import Depends, HTTPException, status, Header
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests
from urllib.parse import urlencode

from typing import List
from resources.resource import UsersResource, User, Insert
from database.database import Database
from admin_check import get_current_admin

from jose import jwt, JWTError

# Database connection
connection_string = ""
database = Database(connection_string)

app = FastAPI()

# Oath section
# Google OAuth2 Config
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8012/auth/callback"
SCOPES = "openid email profile"
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{AUTHORIZATION_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}",
    tokenUrl=TOKEN_URL,
    scopes={"openid": "OpenID Connect scope"}
)

# In-memory store for authenticated users
authenticated_users = {}

@app.get("/auth/login")
async def login():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "access_type": "offline",
    }
    url = f"{AUTHORIZATION_URL}?{urlencode(params)}"
    return RedirectResponse(url=url)

@app.get("/auth/callback")
async def auth_callback(code: str = None):
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid response from Google")

    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    token_r = requests.post(TOKEN_URL, data=token_data)
    token_r.raise_for_status()
    token_json = token_r.json()
    idinfo = id_token.verify_oauth2_token(token_json["id_token"], google_requests.Request(), CLIENT_ID)

    user_email = idinfo.get('email')
    if not user_email or not user_email.endswith('@columbia.edu'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access only allowed for Columbia University users"
        )
    # Constructing the user data
    username = idinfo["given_name"] + "_" + idinfo["family_name"]
    email = idinfo["email"]

    # Create new user. (Yes, we move it here)
    user_data = Insert(username=username, email=email)
    try:
        created_user = users_resource.create_user(user_data)
    except Exception as exc:
        error_detail = {
            "message": "You are successfully logged in and already signed in",
            "access_token": token_json["access_token"],
            "username": username,
            "email": email
        }
        raise HTTPException(status_code=409, detail=error_detail)

    return {"message": "Login and User created successfully","access_token": token_json["access_token"], "username": username, "email": email}

# User section
users_resource = UsersResource(database)

@app.get("/")
async def root():
    return {"message": "Hello World! This is micro1 microservice for SpaceZ"}

@app.get("/api/docs")
async def get_api_docs():
    return {"message": "API documentation available at /docs"}

@app.get("/api/users", response_model=List[User])
async def get_users():
    return users_resource.get_all_users()

@app.put("/api/users/{email}", response_model=dict)
async def update_user(email: str, new_username: str = Body(..., embed=True), _: dict = Depends(get_current_admin)):
    # JWT token validation is handled by get_current_admin dependency
    return users_resource.update_user(email, new_username)

@app.delete("/api/users/{email}", response_model=dict)
async def delete_user(email: str, _: dict = Depends(get_current_admin)):
    return users_resource.delete_user(email)

# Changed since email is the primary key
@app.get("/api/users/{email}", response_model=User)
async def get_user(email: str):
    return users_resource.get_user(email)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
