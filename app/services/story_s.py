from ..schemas import StorySchema
from ..models import StoryModel
from ..utils.common_funcs import generate_unique_slug, generate_slug


class StoryService:
    @staticmethod
    def create(user_id: int, user: "UserModel", **kwargs):
        errors = StorySchema.validate(**kwargs)
        if errors:
            raise ValueError(errors)
        base_slug = generate_slug(kwargs["title"])
        slugs = StoryModel.filter_by(slug=base_slug).all()
        kwargs["slug"] = generate_unique_slug(kwargs["title"], slugs)
        kwargs["user_id"] = user_id
        kwargs["user"] = user
        story = StoryModel.create(**kwargs)
        return story

    @staticmethod
    def update(story_id, **kwargs):
        errors = StorySchema.validate(**kwargs)
        if errors:
            raise ValueError(errors)

        story = StoryModel.get(story_id)
        story.update(**kwargs)
        return story
