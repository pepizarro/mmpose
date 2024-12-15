
import cv2

video = cv2.VideoCapture(0)
print(video.isOpened())

video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

video.set(cv2.CAP_PROP_FOURCC, 0x32595559)


print(video.get(cv2.CAP_PROP_FPS))
