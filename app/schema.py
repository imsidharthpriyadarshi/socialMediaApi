from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id:Optional[str] = None   
             
class ResponseOnUserCreate(BaseModel):
    email:str
    id:int
    created_at:datetime
    class Config:
        orm_mode = True            
     

class PostBase(BaseModel):
    title : str
    content: str
    published : bool =True
    
 
class Post(PostBase):
    id: int
    created_at:datetime
    owner_id:int
    owner :ResponseOnUserCreate
    
    class Config:
        orm_mode = True    


class PostsOut(BaseModel):
    Post: Post
    likes: int
    class Config:
        orm_mode = True 

class Vote(BaseModel):
    post_id: int
    vote_dir: int
    


class Voteout(Vote):
        post :Post
        user: ResponseOnUserCreate
        
        class Config:
            orm_mode = True