#crud.py
from sqlalchemy.orm import Session
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, username: str, hashed_password: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return None
    db_user.hashed_password = hashed_password
    db.commit()
    return db_user


def create_property(db: Session, property: schemas.PropertyCreate, owner_id: int):
    db_property = models.Property(**property.dict(), owner_id=owner_id)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property



def update_property(db: Session, property_id: int, property: schemas.PropertyUpdate):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        return None
    for var, value in vars(property).items():
        setattr(db_property, var, value) if value else None
    db.commit()
    db.refresh(db_property)
    return db_property


def delete_property(db: Session, property_id: int):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property:
        db.delete(db_property)
        db.commit()
    return db_property

# def get_properties(db: Session):
#     return db.query(models.Property).all()

def get_property(db: Session, property_id: int):
    return db.query(models.Property).filter(models.Property.id == property_id).first()

# Similarly, you would create CRUD operations for tenants and rental applications.

def get_tenants(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Tenant).offset(skip).limit(limit).all()

def get_tenant(db: Session, tenant_id: int):
    return db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()


def create_tenant(db: Session, tenant: schemas.TenantCreate):
    db_tenant = models.Tenant(
        name=tenant.name,
        email=tenant.email,
    )
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant


# Admin-related CRUD operations

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user_role(db: Session, user_id: int, role: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.is_admin = role.lower() == "admin"
        db.commit()
        db.refresh(user)
    return user
# Application-related CRUD operations

def create_application(db: Session, application: schemas.RentalApplicationCreate):
    db_application = models.RentalApplication(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_application(db: Session, application_id: int):
    return db.query(models.RentalApplication).filter(models.RentalApplication.id == application_id).first()

def update_application_status(db: Session, application_id: int, status: str):
    application = db.query(models.RentalApplication).filter(models.RentalApplication.id == application_id).first()
    if application:
        application.status = status
        db.commit()
        db.refresh(application)
    return application

def list_applications(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.RentalApplication).offset(skip).limit(limit).all()