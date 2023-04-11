import cv2
import os
import shutil

#img_dir = "D:\Comp-Eng-2023\ImageAI\ourCode\images"
#from image_prediction import *

from fastapi import FastAPI

app = FastAPI()

#making an images directory 
directory = "images"
parent_dir = os.getcwd()
img_dir = os.path.join(parent_dir, directory)
if os.path.exists(img_dir):
    shutil.rmtree(img_dir)
os.mkdir(img_dir)

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
    
def newest(path): # gets the latest created file
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def predict(dir): # function to call the prediction function
    os.chdir("..")
    os.system('python .\image_prediction.py -f '+ dir)

@app.post("/")
def start_process():
    get_photo()
    dir_newest = newest(path = img_dir)
    predict(dir = dir_newest)
    #return {get_prediction() + " : " + get_probability()}
    return {"process ended successfully"}

# start_process()
# print(get_prediction() + " : " + get_probability())