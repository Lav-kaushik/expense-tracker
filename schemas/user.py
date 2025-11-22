from pydantic import BaseModel , EmailStr 
from datetime import datetime , date

class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    username : str
    email : str
    is_active : bool
    created_at = datetime

    class Config:
        from_attribute = True