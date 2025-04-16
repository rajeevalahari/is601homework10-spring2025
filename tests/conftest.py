"""
File: conftest.py

Overview:
This test configuration file sets up fixtures for database operations, HTTP clients,
user state creation, token generation, and a dummy SMTP (email) stub for testing
a FastAPI application.
"""

# Standard library imports
from builtins import range
from datetime import datetime
from uuid import uuid4
from unittest.mock import patch

# Third-party imports
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session
from faker import Faker

# Application-specific imports
from app.main import app
from app.database import Base, Database
from app.models.user_model import User, UserRole
from app.dependencies import get_db, get_settings
from app.utils.security import hash_password
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService
from app.services.jwt_service import create_access_token

fake = Faker()
settings = get_settings()

# Use the testing database URL (ensuring it uses asyncpg)
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL, echo=settings.debug)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)

# --- SMTP stub fixture ---
# This fixture stubs out email functionality by patching the SMTPClient's methods.
# We check if the SMTPClient has an attribute "login". If it does not, we add our dummy version.
@pytest.fixture(autouse=True, scope="function")
def stub_smtp(monkeypatch):
    from app.utils import smtp_connection

    def dummy_send_email(self, subject, html_content, email):
        # Simply return True to simulate a successful email send.
        return True

    def dummy_login(self, username, password):
        # Simulate a successful login with Mailtrap or any SMTP server.
        return (235, b"2.7.0 Authentication successful")

    # Patch the send_email method.
    monkeypatch.setattr(smtp_connection.SMTPClient, "send_email", dummy_send_email)
    # Check if the SMTPClient class has a 'login' attribute; if not, add it.
    if not hasattr(smtp_connection.SMTPClient, "login"):
        setattr(smtp_connection.SMTPClient, "login", dummy_login)

# --- Email Service Fixture ---
@pytest.fixture
def email_service():
    # Assuming TemplateManager doesn't require extra arguments.
    template_manager = TemplateManager()
    email_service = EmailService(template_manager=template_manager)
    return email_service

# --- Async HTTP client fixture ---
@pytest.fixture(scope="function")
async def async_client(db_session):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        app.dependency_overrides[get_db] = lambda: db_session
        try:
            yield client
        finally:
            app.dependency_overrides.clear()

# --- Database initialization fixture ---
@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    try:
        Database.initialize(settings.database_url)
    except Exception as e:
        pytest.fail(f"Failed to initialize the database: {str(e)}")

# --- Setup and teardown database for each test function ---
@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        # Comment this line out during development if you wish to keep the data for debugging.
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

# --- Database session fixture ---
@pytest.fixture(scope="function")
async def db_session(setup_database):
    async with AsyncSessionScoped() as session:
        try:
            yield session
        finally:
            await session.close()

# --- User Fixtures for different states ---
@pytest.fixture(scope="function")
async def locked_user(db_session):
    unique_email = fake.email()
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": unique_email,
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": True,
        "failed_login_attempts": settings.max_login_attempts,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def user(db_session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": False,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def verified_user(db_session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": True,
        "is_locked": False,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def unverified_user(db_session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.user_name(),  # can also use fake.first_name() if desired
        "last_name": fake.user_name(),
        "email": fake.email(),
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": False,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def users_with_same_role_50_users(db_session):
    users = []
    for i in range(50):
        user_data = {
            "nickname": f"{fake.user_name()}_{i}",  # Ensure uniqueness by appending index
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "hashed_password": fake.password(),  # (Consider hashing if required)
            "role": UserRole.AUTHENTICATED,
            "email_verified": False,
            "is_locked": False,
        }
        user = User(**user_data)
        db_session.add(user)
        users.append(user)
    await db_session.commit()
    return users

@pytest.fixture
async def admin_user(db_session: AsyncSession):
    user = User(
        nickname="admin_user",
        email="admin@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password="securepassword",
        role=UserRole.ADMIN,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture
async def manager_user(db_session: AsyncSession):
    user = User(
        nickname="manager_john",
        first_name="John",
        last_name="Doe",
        email="manager_user@example.com",
        hashed_password="securepassword",
        role=UserRole.MANAGER,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

# --- Fixtures for common test data for schemas ---
@pytest.fixture
def user_base_data():
    return {
        "nickname": "john_doe_123",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe",
    }

@pytest.fixture
def user_base_data_invalid():
    return {
        "nickname": "john_doe_123",
        "email": "john.doe.example.com",  # Invalid email
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe",
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword123!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.new@example.com",
        "first_name": "John",
        "last_name": "H. Doe",
        "bio": "I specialize in backend development with Python and Node.js.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg"
    }

@pytest.fixture
def user_response_data():
    from uuid import uuid4
    now = datetime.now()
    return {
        "id": uuid4(),  # Valid UUID
        "nickname": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "last_login_at": now,
        "created_at": now,
        "updated_at": now,
        "links": []
    }

@pytest.fixture
def login_request_data():
    return {"email": "john_doe_123@example.com", "password": "SecurePassword123!"}

# --- Token fixtures using create_access_token ---
from app.services.jwt_service import create_access_token

@pytest.fixture
def admin_token(admin_user):
    return create_access_token(data={"sub": str(admin_user.id), "role": "ADMIN"})

@pytest.fixture
def manager_token(manager_user):
    return create_access_token(data={"sub": str(manager_user.id), "role": "MANAGER"})

@pytest.fixture
def user_token(user):
    return create_access_token(data={"sub": str(user.id), "role": "AUTHENTICATED"})
