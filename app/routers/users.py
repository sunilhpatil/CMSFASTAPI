from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import models, schemas,utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# create user 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):

    isuser = db.query(models.User).filter(models.User.email==user.email).first()

    if isuser :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already present")

    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass

    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# get user
@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id:int,db : Session = Depends(get_db)):

    userid_detail= db.query(models.User).filter(models.User.id == id).first()

    if not userid_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")

    return userid_detail
