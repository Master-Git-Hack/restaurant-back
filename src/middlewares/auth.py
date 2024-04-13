from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .. import config

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Auth:
    __context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    __scheme = scheme = OAuth2PasswordBearer(tokenUrl="token")
    __user = None

    def __init__(self) -> None:
        pass

    def verify(self, password: str, hashed: str):
        return self.__context.verify(password, hashed)

    @property
    def password(self, password: str):
        return self.__context.hash(password)

    def authenticate(self, username: str, password: str):
        if not self.__user.filter(username=username):
            return False
        if not self.verify(password=password, hashed=self.__user.password):
            return False
        return self.__user.to_dict()

    def create_token(self, sub: str, expires_delta: timedelta | None = None, **data):
        data["sub"] = sub
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(hours=12)
        data["exp"] = expire
        return jwt.encode(data, **config.JWT.encode_params)

    def current_user(self, token: Annotated[str, Depends(__scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, **config.JWT.decode_params)
            username: str = payload.get("sub")
            if not self.__user.filter(username=username):
                raise credentials_exception
            return self.__user.to_dict()

        except JWTError:
            raise credentials_exception
