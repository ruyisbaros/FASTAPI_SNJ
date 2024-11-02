from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .schemas import TokenData

# Set your own secret key and algorithm
SECRET_KEY = "dfhgfn875454&!&&54389??&$§§§§§§§§"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=300)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, "HS256")

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        # print(payload["user_id"])
        if payload["user_id"] is None:
            raise credentials_exception

        # token_data = TokenData(id=id)
        return payload

    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)


def get_current_user2(request: Request):
    token = request.cookies.get("access_token")
    print(token)
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        if payload.user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"payload": payload}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
