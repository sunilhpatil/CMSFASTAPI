from typing import Optional, List
from fastapi import  HTTPException, Response, status, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session


from .. import models, schemas,oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#get posts
@router.get("/", response_model= List[schemas.PostOut])
def get_posts( db : Session = Depends(get_db),
              current_user : int = Depends(oauth2.get_current_user), 
              limit:int =10, skip = 0, search : Optional[str]=""):

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
   
    
    if not posts:
        raise HTTPException (status_code= status.HTTP_204_NO_CONTENT, detail=f"No posts yet added")

    return posts  #posts


#get single post
@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id:int, db : Session = Depends(get_db),
             current_user : int = Depends(oauth2.get_current_user)):

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return post

# create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post : schemas.PostCreate, db : Session = Depends(get_db), 
                current_user : int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# delete post
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db), 
                current_user : int = Depends(oauth2.get_current_user)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()
   

    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.owner_id != int(current_user.id):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")
    

    
    deleted_post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db : Session = Depends(get_db),
                 current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()

    if old_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if old_post.owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()