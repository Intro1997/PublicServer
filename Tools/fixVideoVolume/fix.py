import os
from moviepy.editor import VideoFileClip
        
# def batch_volumex(path, x):
#     # 函数功能：在指定路径下，将该文件夹的视频声音调为x倍
#     origin_path = os.getcwd()
#     os.chdir(path)
#     for fname in os.listdir():
#         clip = VideoFileClip(fname)
#         newclip = clip.volumex(x)
#         newclip.write_videofile("new_"+fname)
#     os.chdir(origin_path)
# batch_volumex(path, 5)


file_path = "./GAMES102_P1.mp4"
ret_file_path = "./new_" + os.path.basename(file_path)
print("output to ", ret_file_path)
clip = VideoFileClip(file_path)
newclip = clip.volumex(12)
newclip.write_videofile(ret_file_path)