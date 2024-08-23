#application.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import get_current_active_user
from app.schemas import RentalApplicationCreate, RentalApplicationRead, RentalApplicationUpdate
from app.crud import create_application, get_application, update_application_status, list_applications
from app.models import User, RentalApplication



router = APIRouter()

@router.post("/", response_model=RentalApplicationRead)
def submit_application(application: RentalApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    db_application = create_application(db=db, application=application)
    return db_application

@router.get("/{application_id}", response_model=RentalApplicationRead)
def get_application_endpoint(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    application = get_application(db=db, application_id=application_id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    if application.tenant.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this application")
    return application

@router.put("/{application_id}/status", response_model=RentalApplicationRead)
def update_application_status_endpoint(application_id: int, status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    application = get_application(db=db, application_id=application_id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update application status")
    updated_application = update_application_status(db=db, application_id=application_id, status=status)
    return updated_application

@router.get("/", response_model=list[RentalApplicationRead])
def list_applications_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    applications = list_applications(db=db, skip=skip, limit=limit)
    return applications
