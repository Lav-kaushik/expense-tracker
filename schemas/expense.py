from pydantic import BaseModel , EmailStr 
from datetime import datetime , date

class ExpenseBase(BaseModel):
    item_name : str
    amount : float
    category : str

class ExpenseCreate(ExpenseBase):
    date : date

class ExpenseOut(ExpenseBase):
    id : int
    user_id : int
    amount : int
    date : datetime
    created_at : datetime

    class Config:
        from_attribute = True