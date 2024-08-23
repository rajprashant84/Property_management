#model.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Define relationship to Properties and Tenants
    properties = relationship("Property", back_populates="owner")
    tenants = relationship("Tenant", back_populates="user")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    location = Column(String, index=True)
    number_of_bedrooms = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Set up the reverse relationship to User and to RentalApplication
    owner = relationship("User", back_populates="properties")
    rental_applications = relationship("RentalApplication", back_populates="property")

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)  # Ensure email is unique if required
    user_id = Column(Integer, ForeignKey("users.id"))

    # Set up the reverse relationship to User
    user = relationship("User", back_populates="tenants")
    rental_applications = relationship("RentalApplication", back_populates="tenant")

class RentalApplication(Base):
    __tablename__ = "rental_applications"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))
    status = Column(String, default="pending")
    submission_date = Column(DateTime, default=datetime.utcnow)

    # Set up the relationships to Tenant and Property
    tenant = relationship("Tenant", back_populates="rental_applications")
    property = relationship("Property", back_populates="rental_applications")



