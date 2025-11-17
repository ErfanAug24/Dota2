from ..models.follow import FollowModel


class FollowService:
    @staticmethod
    def follow(
        user_id: int, target_id: int, follower: "UserModel", followed: "UserModel"
    ) -> FollowModel:
        """
        Follow another user by creating a FollowModel entry.
        Raises if already followed.
        """
        if user_id == target_id:
            raise ValueError("You cannot follow yourself.")

        existing = FollowModel.filter_by(
            follower_id=user_id, followed_id=target_id
        ).first()
        if existing:
            raise ValueError(f"You already followed {followed.fullname}")
        follow_instance = FollowModel.create(
            follower_id=follower.id,
            follower=follower,
            followed_id=followed.id,
            followed=followed,
        )
        return follow_instance

    @staticmethod
    def unfollow(user_id: int, target_id: int, followed: "UserModel") -> None:
        """
        Unfollow another user.

        Raises:
            ValueError: if trying to unfollow oneself or not already following the user.
        """
        if user_id == target_id:
            raise ValueError("You cannot unfollow yourself.")
        existing = FollowModel.filter_by(
            follower_id=user_id, followed_id=target_id
        ).first()
        if not existing:
            raise ValueError(f"You are not following {followed.fullname}")
        existing.remove()
