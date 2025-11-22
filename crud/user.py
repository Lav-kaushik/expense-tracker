from sqlalchemy.orm import Session
from sqlalchemy import select , update , delete
from schemas import UserCreate , UserOut
from models.user import User
from security import secure

# create user
# get user by id
# get user by email
# update / delete user

def create_user(db:Session , user_data:UserCreate) -> User:
    hashed_passwd = secure.hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email = user_data.email,
        hashed_password = hashed_passwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user_by_id(db:Session , user_id:int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt).scalar_one_or_none()
    return result

def get_user_by_email(db:Session , user_email:str) -> User | None:
    stmt = select(User).where(User.email==user_email)
    result = db.execute(stmt).scalar_one_or_none()
    return result

def get_user_by_name(db:Session , user_name:str) -> User | None:
    stmt = select(User).where(User.username==user_name)
    result = db.execute(stmt).scalar_one_or_none()
    return result

def update_user(db:Session , user_id:int , user_data:UserCreate) -> User | None:
    hashed_passwd = secure.hash_password(user_data.password)
    stmt = update(User).where(User.id==user_id).values(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_passwd
    )

    db.execute(stmt)
    db.commit()

    updated_user = db.execute(select(User.id == user_id)).scalar_one_or_none()  
    return updated_user

def delete_user(db:Session , user_id:int) -> dict[str , str]:
    stmt = update(User).where(User.id==user_id).values(
        is_active = False
    )
    db.execute(stmt)
    db.commit()

    return {"Message":"User Deleted Successfully."}