from ..models.like import LikeModel


class LikeService:
    @staticmethod
    def like(
        story_id: int, user_id: int, story: "StoryModel", user: "UserModel"
    ) -> LikeModel:
        liked = LikeModel.filter_by(user_id=user_id, story_id=story_id).first()
        if liked:
            raise ValueError(f"You already liked Story : {story.title}")
        like_instance = LikeModel.create(
            user_id=user_id, user=user, story_id=story_id, story=story
        )
        return like_instance

    @staticmethod
    def unlike(story_id: int, user_id: int, story: "StoryModel") -> None:
        liked = LikeModel.filter_by(user_id=user_id, story_id=story_id).first()
        if not liked:
            raise ValueError(f"You are not liking Story : {story.title}")
        liked.remove()
