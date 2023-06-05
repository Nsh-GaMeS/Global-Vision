import sys
sys.path.append("..")

import os
import shutil
import cv2
from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/resourceurl",
    tags=["resourceurl"],
    responses={404: {"description": "Not found"}}
)

class photoBitMap(BaseModel):
    photo: str

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class ResourceUrl(BaseModel):
    url_with_query_string: str


# @router.get("/")
# async def get_all(db: Session = Depends(get_db)):
#     return db.query(models.ResourceUrl).all()

#making an images directory 
directory = "images"
parent_dir = os.getcwd()
img_dir = os.path.join(parent_dir, directory)
if os.path.exists(img_dir):
    shutil.rmtree(img_dir)
os.mkdir(img_dir)

@router.get("/take_photo_locally")
def get_photo(): # function to take a photo and save it to "images" folder
    img_counter = 0
    directory = img_dir # path to the images folder  
    cam = cv2.VideoCapture(0) #set the capture device to default 
    
    cv2.namedWindow("test") # name the video window

    while True:
        #frezzes the frame if something failed 
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        #ends the get_photo function if ESC is pressed (27 in ascii)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        #saves the images to the imags folder if space key is pressed (32 in ascii)
        elif k%256 == 32:
            os.chdir(directory)
            # SPACE pressed
            img_name = "frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    #once done, release the capture device and close the window
    cam.release()
    cv2.destroyAllWindows()

@router.get("/get_path")
def get_path():
    return img_dir

@router.get("/{resource_url_with_query_string}")
async def get_resourceurl(resource_url_with_query_string: str,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    resourceurl_model = db.query(models.ResourceUrl)\
        .filter(models.ResourceUrl.url_with_query_string == resource_url_with_query_string)\
        .first()
    if resourceurl_model is not None:
        return resourceurl_model
    raise http_exception()

@router.get("/newest_file")
def newest(path): # gets the latest created file
     files = os.listdir(path)
     paths = [os.path.join(path, basename) for basename in files]
     return max(paths, key=os.path.getctime)

@router.post("/")
async def create_resourceurl(resourceurl: ResourceUrl,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    resourceurl_model = models.ResourceUrl()
    resourceurl_model.url_with_query_string = resourceurl.url_with_query_string

    db.add(resourceurl_model)
    db.commit()

    return successful_response(201)

@router.get("/predict")
def predict(dir): # function to call the prediction function
    os.chdir("..")
    os.system('python .\image_prediction.py -f '+ dir)

@router.post("/start_process")
def start_process():
    get_photo()
    dir_newest = newest(path = img_dir)
    predict(dir = dir_newest)
    #return {get_prediction() + " : " + get_probability()}
    return {"process ended successfully"}

@router.put("/get_photo")
def get_photo_from_app(photo: photoBitMap):
    bitmap = photo.photo
    print(bitmap)
    return bitmap

def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="ResourceURL not found in users DB")

