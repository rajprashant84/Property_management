#schemas.py
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# Pydantic model for user creation
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True  # Pydantic V2 compatibility

# Define the base schema for properties
class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    location: str
    number_of_bedrooms: int

# Schema for creating a new property
class PropertyCreate(PropertyBase):
    pass

# Schema for reading property data (including ID and owner_id)
class PropertyRead(PropertyBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Pydantic V2 compatibility

# Schema for updating an existing property
class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    number_of_bedrooms: Optional[int] = None

# Pydantic model for tenant
class TenantBase(BaseModel):
    name: str
    email: EmailStr

class TenantCreate(TenantBase):
    pass

# schemas.py
class TenantRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    #user_id: Optional[int] = None  # Make user_id optional or remove it if not needed

    class Config:
        orm_mode = True


# Pydantic model for rental application creation
class RentalApplicationBase(BaseModel):
    tenant_id: int
    property_id: int

class RentalApplicationCreate(RentalApplicationBase):
    pass

class RentalApplicationRead(RentalApplicationBase):
    id: int
    status: str
    submission_date: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pydantic V2 compatibility

# Pydantic model for rental application update
class RentalApplicationUpdate(BaseModel):
    status: Optional[str] = None

# Pydantic model for token data
class TokenData(BaseModel):
    username: Optional[str] = None  # Use Optional[str] for Python 3.9 compatibility

class Token(BaseModel):
    access_token: str
    token_type: str


