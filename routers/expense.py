from fastapi import APIRouter , Depends , HTTPException
from schemas.expense import ExpenseOut , ExpenseCreate
from sqlalchemy.orm import Session
from crud import expense as expense_crud
from database import get_db


router = APIRouter(prefix='/expense' , tags=["Expense"])

@router.post("/" , response_model=ExpenseOut)
def create_Expense(expense:ExpenseCreate , db:Session = Depends(get_db) , user_id=1):
    return expense_crud.create_expense(db , user_id , expense)


@router.get('/{expense_id}' , response_model=ExpenseOut)
def list_by_id(expense_id:int , db:Session = Depends(get_db) , user_id=1):
    result = expense_crud.list_by_id(db ,user_id , expense_id)
    if not result:
        raise HTTPException(status_code=404 , detail="Expesne Not Found.")
    return result


@router.get('/{category}' , response_model=list[ExpenseOut])
def list_by_category(category:str , user_id=1 , db:Session= Depends(get_db)):
    return expense_crud.list_expenses_by_category(db , category , user_id)


@router.get('/all' , response_model=list[ExpenseOut])
def list_all_expenses(user_id=1 , db:Session= Depends(get_db)):
    result = expense_crud.list_all_expenses(db , user_id)
    if not result:
        raise HTTPException(status_code=404 , detail="Expesne Not Found.")
    return result


@router.get('/list' , response_model=list[ExpenseOut])
def list_expenses(skip:int , limit:int , user_id=1 , db:Session= Depends(get_db)):
    result = expense_crud.list_expenses(db , user_id , skip , limit)
    if not result:
        raise HTTPException(status_code=404 , detail="Expesne Not Found.")
    return result


@router.put('/{expense_id}' , response_model=ExpenseOut)
def update_expense(expense_id:int , expense_data:ExpenseCreate , db:Session= Depends(get_db) , user_id=1):
    result = expense_crud.update_expense(db , expense_id , expense_data)
    if not result:
        raise HTTPException(status_code=404 , detail="Expesne Not Found.")
    return result


@router.delete('/{expense_id}')
def delete_expesne(expense_id:int , db:Session= Depends(get_db) , user_id=1):
    result = expense_crud.delete(db , expense_id)
    if not result:
        raise HTTPException(status_code=404 , detail="Expesne Not Found.")
    return result
