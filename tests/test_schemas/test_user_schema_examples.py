# tests/test_schemas/test_user_schema_examples.py

import pytest
from uuid import UUID
from app.schemas.user_schemas import UserBase, UserCreate, UserResponse, LoginRequest

def test_userbase_field_examples():
    """
    Verify that the example metadata for key fields in the UserBase schema is as expected.
    """
    schema = UserBase.model_json_schema()
    properties = schema.get("properties", {})

    # Check for first_name example
    expected_first_name_example = "John"
    actual_first_name_example = properties.get("first_name", {}).get("example")
    assert actual_first_name_example == expected_first_name_example, (
        f"Expected first_name example to be '{expected_first_name_example}', but got '{actual_first_name_example}'"
    )

    # Check for email example
    expected_email_example = "john.doe@example.com"
    actual_email_example = properties.get("email", {}).get("example")
    assert actual_email_example == expected_email_example, (
        f"Expected email example to be '{expected_email_example}', but got '{actual_email_example}'"
    )

    # For nickname, verify that the example exists and is a non-empty string.
    actual_nickname_example = properties.get("nickname", {}).get("example")
    assert isinstance(actual_nickname_example, str) and actual_nickname_example.strip() != "", (
        "Expected a non-empty string for nickname example"
    )

def test_usercreate_field_examples():
    """
    Verify that the example metadata in the UserCreate schema is as expected.
    """
    schema = UserCreate.model_json_schema()
    properties = schema.get("properties", {})

    # Check the email example
    expected_email_example = "john.doe@example.com"
    actual_email_example = properties.get("email", {}).get("example")
    assert actual_email_example == expected_email_example, (
        f"Expected UserCreate.email example to be '{expected_email_example}', but got '{actual_email_example}'"
    )

    # Check the password example
    expected_password_example = "Secure*1234"
    actual_password_example = properties.get("password", {}).get("example")
    assert actual_password_example == expected_password_example, (
        f"Expected UserCreate.password example to be '{expected_password_example}', but got '{actual_password_example}'"
    )

def test_userresponse_field_examples():
    """
    Verify that the example metadata in the UserResponse schema is as expected.
    """
    schema = UserResponse.model_json_schema()
    properties = schema.get("properties", {})

    # Check that the id example is a valid UUID.
    id_example = properties.get("id", {}).get("example")
    try:
        UUID(str(id_example))
    except Exception:
        pytest.fail(f"UserResponse.id example '{id_example}' is not a valid UUID")

    # Check the role example
    expected_role_example = "AUTHENTICATED"
    actual_role_example = properties.get("role", {}).get("example")
    assert actual_role_example == expected_role_example, (
        f"Expected UserResponse.role example to be '{expected_role_example}', but got '{actual_role_example}'"
    )

def test_loginrequest_field_examples():
    """
    Verify that the example metadata in the LoginRequest schema is as expected.
    """
    schema = LoginRequest.model_json_schema()
    properties = schema.get("properties", {})

    # Check the email example for LoginRequest
    expected_email_example = "john.doe@example.com"
    actual_email_example = properties.get("email", {}).get("example")
    assert actual_email_example == expected_email_example, (
        f"Expected LoginRequest.email example to be '{expected_email_example}', but got '{actual_email_example}'"
    )

    # Check the password example for LoginRequest
    expected_password_example = "Secure*1234"
    actual_password_example = properties.get("password", {}).get("example")
    assert actual_password_example == expected_password_example, (
        f"Expected LoginRequest.password example to be '{expected_password_example}', but got '{actual_password_example}'"
    )
