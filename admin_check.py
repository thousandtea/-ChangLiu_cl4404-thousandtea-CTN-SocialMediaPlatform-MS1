from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta

from fastapi import FastAPI, Response, Path, HTTPException, Body
from fastapi import Depends, HTTPException, status, Header
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer


SECRET_KEY = "Kayn_admin12345"  # Use a strong secret key
ALGORITHM = "HS256"

# Generate a token for admin user
def create_admin_token():
    expire = datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
    to_encode = {"sub": "admin", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_admin(authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized - No token provided")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(token, SECRET_KEY, payload.get("sub"))
        if payload.get("sub") != "admin":
            raise HTTPException(status_code=403, detail="Unauthorized - Not an admin user")
        return payload
    except JWTError as e:
        # Log the specific error for debugging
        print(f"JWT validation error: {e}")
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")

# Below codes are the testing code. Since we are just a small project, we can use it to get token directly.
# In future studies, we need to upgrade it to use more secured methods.
admin_token = create_admin_token()
print(admin_token)

try:
    payload = get_current_admin(f"Bearer {admin_token}")
    print("Authentication successful. Admin payload:", payload)
except Exception as e:
    print("Authentication failed:", str(e))