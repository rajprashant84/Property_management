# tenants.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas, database
from app.security import get_current_active_user  # Ensure only authenticated users can access

router = APIRouter()


@router.post("/", response_model=schemas.TenantRead)
def create_tenant(
    tenant: schemas.TenantCreate,
    db: Session = Depends(database.get_db)
):
    # Check if the email is already registered
    existing_tenant = db.query(models.Tenant).filter(models.Tenant.email == tenant.email).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Email is already registered")

    return crud.create_tenant(db=db, tenant=tenant)

@router.get("/", response_model=List[schemas.TenantRead])
def read_tenants(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_tenants(db, skip=skip, limit=limit)

@router.get("/{tenant_id}", response_model=schemas.TenantRead)
def read_tenant(tenant_id: int, db: Session = Depends(database.get_db)):
    db_tenant = crud.get_tenant(db, tenant_id=tenant_id)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant

# @router.post("/", response_model=schemas.TenantRead)
# def create_tenant(
#     tenant: schemas.TenantCreate, 
#     db: Session = Depends(database.get_db), 
#     current_user: schemas.UserRead = Depends(get_current_active_user)
# ):
#     # Ensure the current user is authenticated and has necessary privileges
#     if not current_user.is_admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create tenant")
    
#     return crud.create_tenant(db=db, tenant=tenant)

# @router.get("/", response_model=List[schemas.TenantRead])
# def read_tenants(
#     skip: int = 0, 
#     limit: int = 10, 
#     db: Session = Depends(database.get_db), 
#     current_user: schemas.UserRead = Depends(get_current_active_user)
# ):
#     # Ensure the current user is authenticated
#     if not current_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
#     return crud.get_tenants(db, skip=skip, limit=limit)

# @router.get("/{tenant_id}", response_model=schemas.TenantRead)
# def read_tenant(
#     tenant_id: int, 
#     db: Session = Depends(database.get_db), 
#     current_user: schemas.UserRead = Depends(get_current_active_user)
# ):
#     # Ensure the current user is authenticated
#     if not current_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

#     db_tenant = crud.get_tenant(db, tenant_id=tenant_id)
#     if db_tenant is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    
#     # Ensure that the tenant belongs to the current user or the user is an admin
#     if db_tenant.user_id != current_user.id and not current_user.is_admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this tenant")

#     return db_tenant

