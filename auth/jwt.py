from fastapi import Depends , HTTPException , status
from jose import JWTError , jwt
from sqlalchemy.orm import Session
from database import get_db
from crud.user import get_user_by_id
from dependency import oauth2_scheme
from dotenv import load_dotenv
import os

def get_current_user(db:Session = Depends(get_db) , token:str = Depends(oauth2_scheme)):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate Credentials."
    )

    try:
        payload = jwt.decode(token , os.getenv("JWT_SECRET_KEY") , algorithms=os.getenv("JWT_ALGORITHM"))
        user_id : str = payload.get("sub")

    except JWTError:
        raise credential_exception
    
    user = get_user_by_id(db=db , user_id=int(user_id))

    if user is None or user.is_active==False:
        raise credential_exception
    
    return user

