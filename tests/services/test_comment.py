from app.services.comment_s import CommentService
import pytest


from app.models import StoryModel, UserModel


@pytest.fixture()
def user():
    return UserModel.create(
        username="JillValentine", email="Jill@gmail.com", fullname="Jill Valentine"
    )


@pytest.fixture()
def story(user):
    return StoryModel.create(
        title="Jill Valentine",
        content="Jill Valentine",
        slug="jill-valentine",
        user_id=user.id,
        user=user,
    )


def test_create_comment(session, user, story):
    comment = CommentService.create(
        content="Fuck your post",
        user_id=user.id,
        user=user,
        story_id=story.id,
        story=story,
    )
    reply = CommentService.create(
        content="what the fuck do you mean",
        user_id=user.id,
        user=user,
        story_id=story.id,
        story=story,
        parent_id=comment.id,
        parent=comment,
    )
    reply_to_reply = CommentService.create(
        content="what on earth are you talking about",
        user_id=user.id,
        user=user,
        story_id=story.id,
        parent=reply,
        parent_id=reply.id,
    )
    assert comment.story_id == story.id
    assert comment.user_id == user.id
    assert reply_to_reply.parent_id == reply.id


def test_update_comment(session, user, story):
    comment = CommentService.create(
        content="Fuck your post",
        user_id=user.id,
        user=user,
        story_id=story.id,
        story=story,
    )
    comment.content = "Updated content"
    assert comment.content == "Updated content"


def test_delete_comment(session, user, story):
    comment = CommentService.create(
        content="Fuck your post",
        user_id=user.id,
        user=user,
        story_id=story.id,
        story=story,
    )

    assert comment.remove()
