import pytest
from app.extensions import redis_client
from app.services.auth_s import UserAuthentication, UserPasswordService
from app.models import UserModel

username = "john"
email = "johnwick@gmail.com"
password = "kill3with1pencil"
fullname = "john wick"


@pytest.fixture()
def sample_user(session):
    return UserAuthentication().sign_up(username, email, password, fullname)


def test_signup(session, sample_user):
    fetched = UserModel.get(sample_user.id)
    assert fetched.id == sample_user.id


def test_signup_input_error(session):
    with pytest.raises(ValueError) as excinfo:
        UserAuthentication().sign_up(username, "johnwick.com", "seven", fullname)

    message = str(excinfo.value)
    assert "Invalid email format" in message
    assert "Password must be at least 8 characters long" in message


def test_signup_with_duplicate_values(session):
    with pytest.raises(ValueError, match=f"username '{username}' already exists."):
        UserAuthentication().sign_up(username, email, password, fullname)
        UserAuthentication().sign_up(username, email, password, fullname)


def test_signin(session, sample_user):
    user = UserAuthentication().sign_in(email, password)
    assert user.id == sample_user.id


def test_signin_wrong_password(session, sample_user):
    with pytest.raises(ValueError, match="Wrong password."):
        UserAuthentication().sign_in(email, "kill3with2pencil")


def test_signin_wrong_email(session, sample_user):
    email = "excommunitywick@gmail.com"
    with pytest.raises(LookupError, match=f"No user found with email={email}"):
        UserAuthentication().sign_in(email, "123456789a")


def test_reset_password_token_generation(session, sample_user):
    token = UserPasswordService().initiate_password_reset(sample_user.email)
    assert token is not None


def test_rest_token_validation(session, sample_user):
    token = UserPasswordService().initiate_password_reset(sample_user.email)
    assert UserPasswordService().validate_reset_token(sample_user.email, token) == True


def test_reset_password(session, sample_user):
    token = UserPasswordService().initiate_password_reset(sample_user.email)
    new_password = "kill3with2pencil"
    UserPasswordService().reset_password(sample_user.email, token, new_password)
    assert (
        UserAuthentication().sign_in(sample_user.email, new_password).id
        == sample_user.id
    )
    with pytest.raises(ValueError, match="Wrong password."):
        UserAuthentication().sign_in(sample_user.email, "wrong2pass")

    assert redis_client.get(f"password_reset_{sample_user.email}") is None


def test_same_passwords(session, sample_user):
    with pytest.raises(
        ValueError, match="New password cannot be the same with the last password."
    ):
        token = UserPasswordService().initiate_password_reset(sample_user.email)
        UserPasswordService().reset_password(sample_user.email, token, password)


def test_change_password(session, sample_user):
    new_password = "erfan261384"
    UserPasswordService().change_password(sample_user.email, password, new_password)
    user = UserAuthentication().sign_in(sample_user.email, new_password)
    assert user.passwords[:-1] == sample_user.passwords[:-1]
