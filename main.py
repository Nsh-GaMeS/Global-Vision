import cv2
import os

directory = "D:\Comp-Eng-2023\ImageAI\ourCode\images"
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

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
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
# os.system('python D:\Comp-Eng-2023\ImageAI\ImageAI\examples\image_prediction.py -f \car1.jpg')
print("hello")