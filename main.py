import cv2
import os

img_dir = "D:\Comp-Eng-2023\ImageAI\ourCode\images"


def get_photo(): # method to take a photo and save it to "images" folder
    img_counter = 0
    directory = "D:\Comp-Eng-2023\ImageAI\ourCode\images"
    cam = cv2.VideoCapture(0)
    
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        elif k%256 == 32:
            os.chdir(directory)
            # SPACE pressed
            img_name = "frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()
    
def newest(path): # gets the latest created file
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def predict(dir):
    os.chdir("..")
    os.system('python .\image_prediction.py -f '+ dir)

get_photo()
dir_newest = newest(path = img_dir)
predict(dir = dir_newest)
