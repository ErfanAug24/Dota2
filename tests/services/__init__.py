import pytest

from app.models import StoryModel, UserModel


@pytest.fixture()
def user():
    return UserModel.create("JillValentine", "Jill@gmail.com", "Jill Valentine")


@pytest.fixture()
def story(user):
    return StoryModel.create(
        title="Jill Valentine",
        content="Jill Valentine",
        slug="jill-valentine",
        user_id=user.id,
        user=user,
    )
