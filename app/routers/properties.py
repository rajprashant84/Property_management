from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.security import get_current_active_user



router = APIRouter()

@router.post("/", response_model=schemas.PropertyRead)
def create_property(
    property: schemas.PropertyCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_active_user)
):
    # Ensure that the current user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Create a new property with the current user as the owner
    db_property = crud.create_property(db=db, property=property, owner_id=current_user.id)
    return db_property

@router.put("/{property_id}", response_model=schemas.PropertyRead)
def update_property(property_id: int, property: schemas.PropertyUpdate, db: Session = Depends(get_db)):
    db_property = crud.get_property(db=db, property_id=property_id)
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    for key, value in property.dict(exclude_unset=True).items():
        setattr(db_property, key, value)
    db.commit()
    db.refresh(db_property)
    return db_property


@router.delete("/{property_id}")
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_active_user)
):
    # Ensure that the property belongs to the current user or the user is an admin
    db_property = crud.get_property(db=db, property_id=property_id)
    if not db_property or (db_property.owner_id != current_user.id and not current_user.is_admin):
        raise HTTPException(status_code=403, detail="Not authorized to delete this property")
    
    # Delete the property
    return crud.delete_property(db=db, property_id=property_id)

@router.get("/", response_model=List[schemas.PropertyRead])
def list_properties(db: Session = Depends(get_db)):
    return crud.get_properties(db=db)


