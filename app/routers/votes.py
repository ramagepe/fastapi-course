from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from ..db import get_session
from ..models import Post, User, Vote
from ..schemas import VoteIn
from ..utils.handlers import locked_exception, not_found_exception
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def vote_post(
        new_vote: VoteIn,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session)):

    found_post = session.exec(
        select(Post)
        .where(
            Post.id == new_vote.post_id)
    ).first()

    if not found_post:
        not_found_exception("Post does not exist")

    found_vote = session.exec(
        select(Vote)
        .where(
            (Vote.post_id == new_vote.post_id) &
            (Vote.user_id == current_user.id))
    ).first()

    if found_vote and new_vote.is_upvote:
        locked_exception("Already voted on this post.")
    if not found_vote and not new_vote.is_upvote:
        not_found_exception("Cannot remove non-existent vote.")

    if found_vote:
        session.delete(found_vote)
        session.commit()
        return {"message": "Vote successfully deleted."}
    else:
        vote = Vote(post_id=new_vote.post_id, user_id=current_user.id)
        session.add(vote)
        session.commit()
        session.refresh(vote)
        return {"message": "Vote successfully processed."}
