import sys
sys.path.append("..")

# imports
import base64 
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

# router declaretion 
router = APIRouter(
    prefix="/resourceurl",
    tags=["resourceurl"],
    responses={404: {"description": "Not found"}}
)


class photoBitMap(BaseModel):
    photo: str

models.Base.metadata.create_all(bind=engine)

# returns local database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class ResourceUrl(BaseModel):
    url_with_query_string: str

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

# returns the path of an image in the API's host machine
@router.get("/get_path")
def get_path():
    return img_dir

# method to serch through the resourceurl table (not used)
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

# returns newest file on the APIs host machine 
@router.get("/newest_file")
def newest(path): # gets the latest created file
     files = os.listdir(path)
     paths = [os.path.join(path, basename) for basename in files]
     return max(paths, key=os.path.getctime)

# creates the resourcerul table and checks if users still exists  
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

# method to predict image 
@router.get("/predict")
def predict(dir): # function to call the prediction function
    os.chdir("..")
    os.system('python .\image_prediction.py -f '+ dir)

#method to start the capture and prediction proccess localy 
@router.post("/start_process")
def start_process():
    get_photo()
    dir_newest = newest(path = img_dir)
    predict(dir = dir_newest)
    return {"process ended successfully"}

# decode the base64 string into a photo on the local machine
# @router.get("/get_photo/{photo_bitmap}")
# def get_photo_from_app(photo_bitmap: str):
#     #decoded_data=base64.b64decode((photo_bitmap))
#     #write the decoded data back to original format in  file
#     #img_file = open('/images/image.png', 'wb')
#     #img_file.write(decoded_data)
#     print(decoded_data) 

def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="ResourceURL not found in users DB")


