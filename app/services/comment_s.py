from typing import Optional

from ..models import CommentModel


class CommentService:
    @staticmethod
    def create(
        content: str,
        user_id: int,
        user: "UserModel",
        *,
        story_id: Optional[int] = None,
        story: Optional["StoryModel"] = None,
        parent_id: Optional[int] = None,
        parent: Optional["CommentModel"] = None,
    ) -> "CommentModel":
        """
        Create a comment or a reply.
        """
        if story and story_id and story.id == story_id and not parent_id:
            return CommentModel.create(
                content=content,
                user_id=user_id,
                user=user,
                story_id=story_id,
                story=story,
                parent_id=None,
                parent=None,
            )

        elif parent and parent_id and parent.id == parent_id:
            return CommentModel.create(
                content=content,
                user_id=user_id,
                user=user,
                story_id=parent.story_id,
                story=parent.story,
                parent_id=parent_id,
                parent=parent,
            )

        raise ValueError("Invalid comment input: must provide either story or parent.")

    @staticmethod
    def update(content: str, user_id: int, comment_id: int) -> "CommentModel":
        comment = CommentModel.get(comment_id)
        if not comment:
            raise ValueError("Comment not found.")
        if comment.user_id != user_id:
            raise PermissionError("You cannot edit this comment.")
        comment.update(content=content)
        return comment

    @staticmethod
    def delete(comment_id: int, user_id: int) -> None:
        comment = CommentModel.get(comment_id)
        if not comment:
            raise ValueError("Comment not found.")
        if comment.user_id != user_id:
            raise PermissionError("You cannot delete this comment.")

        comment.remove()  # or mark as deleted
