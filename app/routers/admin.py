#admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Property, Tenant, RentalApplication
from app.schemas import UserCreate, UserRead
from app.security import authenticate_user, create_access_token, get_current_active_user, get_password_hash
from app.crud import create_user, get_users, update_user_password, update_user_role

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered. Please use a different username or email."
        )
    # Hash the password and create a new User instance
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,  # Assuming default is active, adjust if your logic differs
        is_admin=False   # Assuming default is not an admin, adjust if your logic differs
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login/", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.debug(f"Attempting to log in user: {form_data.username}")
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Login failed for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"User {form_data.username} logged in successfully")
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.put("/update-password/")
def update_password(username: str, new_password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(new_password)
    return update_user_password(db=db, username=username, hashed_password=hashed_password)

@router.get("/users/", response_model=list[UserRead])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    users = get_users(db=db, skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}/role", response_model=UserRead)
def update_user_role_endpoint(user_id: int, role: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    user = update_user_role(db=db, user_id=user_id, role=role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/analytics/", response_model=dict)
def view_analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    analytics = {
        "total_users": db.query(User).count(),
        "total_properties": db.query(Property).count(),
        "total_tenants": db.query(Tenant).count(),
        "total_applications": db.query(RentalApplication).count(),
    }
    return analytics
