from fastapi import  HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas,oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db : Session = Depends(get_db),
              current_user : int = Depends(oauth2.get_current_user)):
    
    #find post first if exists
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post your are voting for not found")
    
    #vote on post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.vote_dir == 1):
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"User {current_user.id} has already vote on post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exists")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"successfully deleted vote"}
    
