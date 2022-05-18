from fastapi import APIRouter,Depends,status,HTTPException,Response
from .. import schema,database,models,Oauth2
from sqlalchemy.orm import Session



router = APIRouter(
    prefix="/posts",
    tags=["Voting"]
    
)

@router.post("/vote",response_model=schema.Voteout)
def post_vote(voting: schema.Vote ,db:Session = Depends(database.get_db), current_user: schema.UserCreate=Depends(Oauth2.get_current_user) ):
    if not (voting.vote_dir==0 or voting.vote_dir==1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= "plz give valid like response")
    
    if voting.vote_dir==1:
        query = db.query(models.Post).filter(models.Post.id == voting.post_id).first()
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "This post does not exist")
        already_liked_user= db.query(models.Votes).filter(models.Votes.post_id == voting.post_id, models.Votes.user_id== current_user.id)
        if already_liked_user.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= "You already liked this post")
    
        adding_like=models.Votes(user_id= current_user.id, **voting.dict())
        db.add(adding_like)
        db.commit()
        db.refresh(adding_like)
        return adding_like
    
    if voting.vote_dir==0:
        query = db.query(models.Votes).filter(models.Votes.post_id == voting.post_id, models.Votes.user_id== current_user.id)
        if not query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Your like does not exist")
        
        query.delete()
        db.commit()
        return Response(status_code= status.HTTP_204_NO_CONTENT)
    