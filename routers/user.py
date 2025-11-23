from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.orm import Session
from schemas.user import UserCreate , UserOut
from crud import user as user_crud
from database import get_db
from auth import auth
from schemas.auth import LoginSchema

router = APIRouter(prefix='/user' , tags=["User"])

@router.post('/' , response_model=UserOut)
def create_user(user:UserCreate , db:Session = Depends(get_db)):
    result = user_crud.create_user(db=db , user_data=user)
    if not result:
        raise HTTPException(status_code=400 , detail="User already exists or Creation Failed.")
    return result


@router.get('/{user_id}' , response_model=UserOut)
def get_user_by_id(user_id:int , db:Session = Depends(get_db)):
    result = user_crud.get_user_by_id(db=db , user_id=user_id)
    if not result:
        raise HTTPException(status_code=404 , detail="User Not Found.")
    return result


@router.get('/email/{email}' , response_model=UserOut)
def get_user_by_email(email:str , db:Session = Depends(get_db)):
    result = user_crud.get_user_by_email(db=db , user_email=email)
    if not result:
        raise HTTPException(status_code=404 , detail="User Not found.")
    return result


@router.get('/name/{username}' , response_model=UserOut)
def get_user_by_name(username:str , db:Session = Depends(get_db)):
    result = user_crud.get_user_by_name(db=db , user_name=username)
    if not result:
        raise HTTPException(status_code=404 , detail="User Not Found.")
    return result


@router.put('/{user_id}' , response_model=UserOut)
def update_user(user_id:int , user_data:UserCreate , db:Session = Depends(get_db)):
    result = user_crud.update_user(db=db , user_data=user_data , user_id=user_id)
    if not result:
        raise HTTPException(status_code=404 , detail="User not Found or Failed to update Details.")
    return result

@router.delete('/{user_id}')
def delete_user(user_id:int , db:Session = Depends(get_db)):
    result = user_crud.delete_user(db=db , user_id=user_id)
    if not result:
        raise HTTPException(status_code=404 , detail="User not Found or Failed to delete User.")
    return result

@router.post('/login' , response_model=UserOut)
def login_user(credentials:LoginSchema, db:Session = Depends(get_db)):
    user = user_crud.authenticate_user(db=db , email=credentials.email , password=credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid email or password")
    
    access_token = auth.create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


