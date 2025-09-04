from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import EmailStr
from datetime import datetime, timedelta, timezone
from fastapi import Request, HTTPException, status, Depends

from src.config import settings
from src.users.dao import UserDAO

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password_from_user: str, password_in_database: str) -> bool:
    return password_context.verify(password_from_user, password_in_database)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = settings.get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user or verify_password(password_from_user=password, password_in_database=user.password) is False:
        return None
    return user


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = settings.get_auth_data()
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is not valid")
    
    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token has expired")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found")
    
    user = await UserDAO.find_one_or_none(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user