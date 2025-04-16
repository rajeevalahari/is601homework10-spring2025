from builtins import str
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data["first_name"]

# Tests for UserResponse
def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    # assert user.last_login_at == user_response_data["last_login_at"]

# Tests for LoginRequest
def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Tests for UserBase
def test_user_base_invalid_email(user_base_data_invalid):
    with pytest.raises(ValidationError) as exc_info:
        user = UserBase(**user_base_data_invalid)
    
    assert "value is not a valid email address" in str(exc_info.value)
    assert "john.doe.example.com" in str(exc_info.value)

import pytest
from pydantic import ValidationError
from app.schemas.user_schemas import UserBase

@pytest.mark.parametrize("nickname", ["ab", "John Doe", "😀user"])
def test_invalid_nicknames(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

@pytest.mark.parametrize("nickname", ["user123", "john_doe", "Jane-Doe"])
def test_valid_nicknames(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

import pytest
from pydantic import ValidationError
from app.schemas.user_schemas import UserCreate

def test_password_complexity_valid():
    valid_data = {
        "email": "jane.doe@example.com",
        "password": "ValidPass1!",
        "nickname": "janedoe",
    }
    # Should not raise any exception
    user = UserCreate(**valid_data)
    assert user.password == valid_data["password"]

@pytest.mark.parametrize("bad_password", [
    "short",              # Less than 8 characters
    "nocaps123!",         # No uppercase letters
    "NOLOWERCASE123!",    # No lowercase letters
    "NoDigits!",          # No digits
    "NoSpecial123",       # No special characters
])
def test_password_complexity_invalid(bad_password):
    invalid_data = {
        "email": "jane.doe@example.com",
        "password": bad_password,
        "nickname": "janedoe",
    }
    with pytest.raises(ValidationError):
        UserCreate(**invalid_data)

import pytest
from pydantic import ValidationError
from app.schemas.user_schemas import UserBase

@pytest.mark.parametrize("valid_url", [
    "http://example.com/picture.jpg",
    "https://example.com/photo.png",
    None
])
def test_valid_profile_picture_url(valid_url, user_base_data):
    user_base_data["profile_picture_url"] = valid_url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == valid_url

@pytest.mark.parametrize("invalid_url", [
    "ftp://example.com/picture.jpg",  # Invalid scheme
    "example.com/photo.png",          # Missing scheme
    "http:/example.com",              # Malformed scheme
])
def test_invalid_profile_picture_url(invalid_url, user_base_data):
    user_base_data["profile_picture_url"] = invalid_url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)
