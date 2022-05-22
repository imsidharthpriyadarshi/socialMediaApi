from fastapi import APIRouter, File, UploadFile,Depends
from fastapi.responses import FileResponse

from .. import schema,Oauth2
import shutil
import string
import random

router = APIRouter(
    prefix="/file",
    tags= ["File"]
)


@router.post("/image")
def upload_image(image:UploadFile= File(...),current_user : schema.UserCreate=Depends(Oauth2.get_current_user)):
    letters=string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(8))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.',1))
    path = f'photos/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file,buffer)
        
    return {'filename': path}    



@router.get("/download/{name}",response_class=FileResponse)
def get_file(name:str):
    path = f"photos/{name}"
    return path