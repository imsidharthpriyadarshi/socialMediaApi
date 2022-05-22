from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import  Column, ForeignKey,Integer,String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key= True,nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE')
    image_path= Column(String,server_default= 'photos/default.jpg')
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default =text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable = False)
    owner = relationship("User")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,nullable = False)
    email = Column(String, nullable= False,unique =True)
    password = Column(String, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable= False,server_default = text('now()'))
    
    
class Votes(Base):
    __tablename__ = 'votes'
    
    post_id = Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'),nullable = False,primary_key = True)
    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable= False,primary_key= True)
    vote_dir= Column(Integer,nullable = False)
    post = relationship("Post")
    user=relationship("User")
    
        
    
    
    
        