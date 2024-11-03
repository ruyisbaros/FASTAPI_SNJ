from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    new_vote: schemas.Vote,
    db: Session = Depends(get_db),
    payload: dict = Depends(oauth2.get_current_user),
):
    print(new_vote)
    # Check whether  the post exists or  not
    voted_post = (
        db.query(models.Post).filter(models.Post.id == new_vote.post_id).first()
    )
    if voted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    print(voted_post)
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == new_vote.post_id,
        models.Votes.user_id == payload["user_id"],
    )
    found_vote = vote_query.first()
    if new_vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already voted"
            )
        new_vote = models.Votes(post_id=new_vote.post_id, user_id=payload["user_id"])

        db.add(new_vote)
        db.commit()
        return {"message": "Successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="You haven't voted"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully vote reversed"}
