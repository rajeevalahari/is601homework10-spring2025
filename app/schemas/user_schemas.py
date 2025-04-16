# app/schemas/user_schemas.py

from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
from urllib.parse import urlparse

from app.utils.nickname_gen import generate_nickname

class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

def validate_url(url: Optional[str]) -> Optional[str]:
    """
    Validate that the URL (if provided) is a valid HTTP or HTTPS URL.
    It uses urllib.parse.urlparse to check the scheme and netloc.
    """
    if url is None:
        return url
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Invalid URL: must use http or https and include a valid domain")
    return url

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(
        None,
        min_length=3,
        pattern=r'^[\w-]+$',
        example=generate_nickname()
    )
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(
        None,
        example="Experienced software developer specializing in web applications."
    )
    profile_picture_url: Optional[str] = Field(
        None,
        example="https://example.com/profiles/john.jpg"
    )
    linkedin_profile_url: Optional[str] = Field(
        None,
        example="https://linkedin.com/in/johndoe"
    )
    github_profile_url: Optional[str] = Field(
        None,
        example="https://github.com/johndoe"
    )

    # Apply URL validation for the three URL fields.
    _validate_urls = validator(
        'profile_picture_url', 'linkedin_profile_url', 'github_profile_url',
        pre=True, allow_reuse=True
    )(validate_url)
 
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")
    
    @validator("password")
    def password_complexity(cls, password: str) -> str:
        """
        Validate password complexity:
          - Minimum 8 characters.
          - At least one uppercase letter.
          - At least one lowercase letter.
          - At least one digit.
          - At least one special character.
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit.")
        special_characters = "!@#$%^&*()_+-=[]{}|;:'\",.<>?/~`"
        if not any(char in special_characters for char in password):
            raise ValueError("Password must contain at least one special character.")
        return password

class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    nickname: Optional[str] = Field(
        None,
        min_length=3,
        pattern=r'^[\w-]+$',
        example="john_doe123"
    )
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(
        None,
        example="Experienced software developer specializing in web applications."
    )
    profile_picture_url: Optional[str] = Field(
        None,
        example="https://example.com/profiles/john.jpg"
    )
    linkedin_profile_url: Optional[str] = Field(
        None,
        example="https://linkedin.com/in/johndoe"
    )
    github_profile_url: Optional[str] = Field(
        None,
        example="https://github.com/johndoe"
    )

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(
        None,
        min_length=3,
        pattern=r'^[\w-]+$',
        example=generate_nickname()
    )
    # Redefine role here to allow attribute from DB
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    is_professional: Optional[bool] = Field(default=False, example=True)

class LoginRequest(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(
        None,
        example="The requested resource was not found."
    )

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(
        ...,
        example=[{
            "id": uuid.uuid4(),
            "nickname": generate_nickname(),
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "bio": "Experienced developer",
            "profile_picture_url": "https://example.com/profiles/john.jpg", 
            "linkedin_profile_url": "https://linkedin.com/in/johndoe", 
            "github_profile_url": "https://github.com/johndoe",
            "role": "AUTHENTICATED",
            "is_professional": False
        }]
    )
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
