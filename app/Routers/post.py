from typing import List, Optional
from sqlalchemy import func
from .. import models,schema,Oauth2
from fastapi import Depends,status,HTTPException,Response,APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[schema.PostsOut])
def get_posts(db: Session = Depends(get_db),limit:int=10,skip:int=0,search:Optional[str] =""):
    
    result = db.query(models.Post,func.count(models.Votes.post_id).label("likes")).join(models.Votes,models.Post.id== models.Votes.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #cursor.execute("SELECT * FROM posts")
    #posts= cursor.fetchall()
    return  result


@router.get("/get_own_posts",response_model=List[schema.PostsOut])
def get_own_posts(db: Session = Depends(get_db),current_user : schema.UserCreate = Depends(Oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str] =""):
    
    post = db.query(models.Post,func.count(models.Votes.post_id).label("likes")).join(models.Votes,models.Post.id== models.Votes.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search),models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="looks like you have not created any posts")
    return post


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_posts(post :schema.PostBase , db: Session = Depends(get_db),current_user : schema.UserCreate=Depends(Oauth2.get_current_user)):
  
    new_post = models.Post(**post.dict(),owner_id= current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    

    #cursor.execute(""" INSERT INTO posts (title ,content ,published) VALUES(%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    return  new_post
    
    
        
@router.get("/{id}",response_model=schema.PostsOut)
def get_post(id:int,db : Session = Depends(get_db),current_user : schema.UserCreate=Depends(Oauth2.get_current_user)):
    
    post = db.query(models.Post,func.count(models.Votes.post_id).label("likes")).join(models.Votes,models.Post.id== models.Votes.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id ==id).first()
    #cursor.execute("SELECT * FROM posts WHERE id = %s",[str(id)])
    #post=cursor.fetchone()
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Your post is not  exist")    
    return  post
   
   
   
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user : schema.UserCreate=Depends(Oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    #cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *" , [str(id)])
    #delted_post = cursor.fetchone()
    #conn.commit()
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this post does not exist")
    if post.first().owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to delete this post")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
       
       
@router.put("/{id}",response_model=schema.PostsOut)
def update_post(id:int, updated_post: schema.PostBase , db : Session = Depends(get_db),current_user : schema.UserCreate=Depends(Oauth2.get_current_user)):
    post_query =db.query(models.Post).filter(models.Post.id == id)
    #cursor.execute("UPDATE posts SET title = %s, content = %s, published= %s WHERE id = %s RETURNING *" ,(post.title,post.content,post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    if  not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not existed")
    if post_query.first().owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to update this post")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    post= db.query(models.Post,func.count(models.Votes.post_id).label("likes")).join(models.Votes,models.Post.id== models.Votes.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id ==id)
    return post.first()     


