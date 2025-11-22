from sqlalchemy.orm import Session
from sqlalchemy import select , update , delete
from datetime import datetime , timezone
from schemas import expense
from models.expense import Expense

'''
create expense
list expenses
update an expense
delete expense
'''

def create_expense(db:Session , user_id:int , expense_data:expense.ExpenseCreate) -> Expense:
    expense_date = datetime.combine(expense_data.date , datetime.min.time())
    expense_date = expense_date.replace(tzinfo=timezone.utc)

    new_expense = Expense(
        user_id = user_id,
        item_name = expense_data.item_name,
        amount = expense_data.amount,
        category = expense_data.category,
        date = expense_date
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


def list_by_id(db:Session , user_id:int , expense_id:int) -> Expense | None:
    stmt = select(Expense).where(Expense.user_id==user_id , Expense.id == expense_id)
    result = db.exeute(stmt)
    return result


def list_all_expenses(db:Session , user_id:int) -> list[Expense]:
    stmt = select(Expense).where(Expense.user_id == user_id)
    result = db.execute(stmt).scalars.all()
    return result


def list_expenses(db:Session , user_id:int , skip:int=0 , limit:int=10) ->list[Expense]:
    stmt = select(Expense).where(Expense.user_id == user_id).offset(skip).limit(limit)
    result = db.execute(stmt).scalars.all()
    return result


def list_expenses_by_category(db:Session , category:str , user_id=1) -> list[Expense]:
    stmt = select(Expense).where(Expense.user_id==user_id , Expense.category==category)
    result = db.execute(stmt).scalars().all()
    return result


def update_expense(db:Session , user_id:int , expense_id:int , expense_data:expense.ExpenseCreate) -> Expense | None:
    exists = db.execute(select(Expense).where(Expense.user_id==user_id , Expense.id==expense_id)).scalar_one_or_none()
    if not exists:
        return None
    
    expense_date = datetime.combine(expense_data.date, datetime.min.time())
    expense_date = expense_date.replace(tzinfo=timezone.utc)

    stmt = (
        update(Expense)
        .where(Expense.user_id==user_id , Expense.id==expense_id)
        .values(
            item_name = expense_data.item_name,
            amount = expense_data.amount,
            category=expense_data.category,
            date = expense_date
        )
    )

    db.execute(stmt)
    db.commit()
    db.refresh()

    result = db.execute(select(Expense).where(Expense.user_id==user_id , Expense.id==expense_id)).scalar_one()
    return result


def delete_expense(db:Session , user_id:int , expense_id:int) -> dict[str , str]:
    exists = db.execute(select(Expense).where(Expense.user_id==user_id , Expense.id==expense_id)).scalar_one_or_none()
    if not exists:
        return None
    
    stmt = delete(Expense).where(Expense.user_id==user_id , Expense.id==expense_id)
    db.execute(stmt)
    db.commit()
    return {"Message":"Expense Deleted Sucessfully."}


