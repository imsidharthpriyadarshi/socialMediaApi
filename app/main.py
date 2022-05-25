from fastapi import FastAPI
from .Routers import post,user,auth,vote,file
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

#models.Base.metadata.create_all(bind=engine)

app = FastAPI() 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(file.router)


app.mount("/photos",StaticFiles(directory="photos"),name="photos")

@app.get("/")
def sayHello():
    return {"data": "hello deployed successfully"}