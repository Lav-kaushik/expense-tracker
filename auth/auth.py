from jose import jwt
from datetime import datetime , timedelta , timezone
from dotenv import load_dotenv
import os



def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    to_encode.update({"exp":expiry})

    encoded_jwt = jwt.encode(to_encode , os.getenv("JWT_SECRET_KEY") , algorithm=os.getenv("JWT_ALGORITHM"))
    return encoded_jwt