import imageio
import cv2 as cv

input_video_path = "./src_video/v0.mov"
output_gif_path = "./dst_gif/v0.gif"

# reference to https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html#ac4107fb146a762454a8a87715d9b7c96
cap = cv.VideoCapture(input_video_path)
gif = []
while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break
    img = cv.resize(frame, (int(frame.shape[1] / 4), int(frame.shape[0] / 4)))
    gif.append(img)
imageio.mimsave(output_gif_path, gif, 'GIF', duration=1 / 60)
