#auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
import app.schemas as schemas
import app.crud as crud
import app.database as database
import app.security as security
from app.models import User


import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()

# Setup OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = security.get_password_hash(user.password)
    db_user = crud.create_user(db, user=user, hashed_password=hashed_password)
    return db_user

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    user = security.verify_token(token, credentials_exception, db)
    return user

def get_current_admin_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have enough privileges")
    return current_user
