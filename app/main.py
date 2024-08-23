from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.database import Base, engine
from app.routers import properties, admin, application, tenants, auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Property Rental Management Platform")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the OAuth2 scheme
# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")  # Ensure this matches the correct endpoint

# Custom OpenAPI function
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Property Rental Management Platform",
        version="1.0",
        description="API for managing property rentals",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/token",  # Ensure this matches the actual endpoint
                    "scopes": {}
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(properties.router, prefix="/properties", tags=["Property Listings"])
app.include_router(tenants.router, prefix="/tenants", tags=["Tenant Management"])
app.include_router(application.router, prefix="/applications", tags=["Rental Applications"])
app.include_router(admin.router, prefix="/admin", tags=["Admin Dashboard"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Property Management API"}



