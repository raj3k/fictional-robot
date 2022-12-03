from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote_data: schemas.Vote, response: Response, db: Session = Depends(get_db),
               current_user=Depends(oauth2.get_current_user),):

    post_query = db.query(models.Post).filter(models.Post.id == vote_data.post_id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {vote_data.post_id} not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_data.post_id,
                                              models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()
    if vote_data.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote_data.post_id}")
        new_vote = models.Vote(post_id=vote_data.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exist")
        vote_query.delete(synchronize_session="fetch")
        db.commit()
        response.status_code = status.HTTP_200_OK
        return {"message": "successfully deleted vote"}
