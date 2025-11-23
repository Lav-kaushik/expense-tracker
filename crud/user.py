from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from schemas import UserCreate, UserOut
from models.user import User
from security import secure

def create_user(db: Session, user_data: UserCreate) -> User | None:
    try:
        exists = db.execute(select(User).where(User.email == user_data.email)).scalar_one_or_none()
        if exists:
            return None
        hashed_passwd = secure.hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_passwd
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        return None

def get_user_by_id(db: Session, user_id: int) -> User | None:
    try:
        stmt = select(User).where(User.id == user_id)
        result = db.execute(stmt).scalar_one_or_none()
        return result
    except Exception as e:
        db.rollback()
        return None

def get_user_by_email(db: Session, user_email: str) -> User | None:
    try:
        stmt = select(User).where(User.email == user_email)
        result = db.execute(stmt).scalar_one_or_none()
        return result
    except Exception as e:
        db.rollback()
        return None

def get_user_by_name(db: Session, user_name: str) -> User | None:
    try:
        stmt = select(User).where(User.username == user_name)
        result = db.execute(stmt).scalar_one_or_none()
        return result
    except Exception as e:
        db.rollback()
        return None

def update_user(db: Session, user_id: int, user_data: UserCreate) -> User | None:
    try:
        exists = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        if not exists:
            return None
        hashed_passwd = secure.hash_password(user_data.password)
        stmt = update(User).where(User.id == user_id).values(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_passwd
        )
        db.execute(stmt)
        db.commit()
        updated_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        return updated_user
    except Exception as e:
        db.rollback()
        return None

def delete_user(db: Session, user_id: int) -> dict[str, str] | None:
    try:
        exists = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        if not exists:
            return None
        stmt = update(User).where(User.id == user_id).values(is_active=False)
        db.execute(stmt)
        db.commit()
        return {"Message": "User Deleted Successfully."}
    except Exception as e:
        db.rollback()
        return None
    
def authenticate_user(db:Session , email: str , password: str) -> User | None:
    user = get_user_by_email(db=db , user_email=email)
    
    if not user:
        return None
    
    if user.is_active==False:
        return None
    
    if secure.verify_password(plain_pass=password , hashed_pass=user.hashed_password)==False:
        return None
    
    return user