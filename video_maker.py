import cv2
import sys
import dlib
import time
import socket
import struct
import numpy as np
import tensorflow as tf
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
from win32api import GetSystemMetrics
import win32gui

from threading import Thread, Lock
import multiprocessing as mp
from config import get_config
import pickle
import math
import os
import ffmpeg

from moviepy.editor import concatenate_videoclips, VideoFileClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize

import regz_socket_MP_FD
import proj_utils
# regz_socket_MP_FD#.regz([600,300])

conf,_ = get_config()
if conf.mod == 'flx':
    import flx as model
else:
    sys.exit("Wrong Model selection: flx or deepwarp")

# system parameters
model_dir = './'+conf.weight_set+'/warping_model/'+conf.mod+'/'+ str(conf.ef_dim) + '/'
size_video = [640,480]
# size_video = [480,360]
# fps = 0
P_IDP = 5
depth = -50
# for monitoring

# environment parameter
Rs = (GetSystemMetrics(0),GetSystemMetrics(1))


# In[ ]:


model_dir
print(Rs)

# ----------crop zoom video to a single man video----------#

# left top top (108,60)
# left top bottom (637,357)
#
# right bottom top (642,362)
# right bottom bottom (1168,661)

# top right = x_center=905 , y_center=209, width=528, height=299

loops = 4
what_to_do = "compose timing"

if what_to_do == "all" or what_to_do.count("to_align") > 0:
    if __name__ == '__main__':
        clip = VideoFileClip("ziv-meet.MP4")
        newClip = crop(clip, x_center=905 , y_center=209, width=396, height=297)
        newClip = newClip.resize((640,480))
        newClip.write_videofile('to_aline.MP4')

# this is how to call the regz_socket_MP_FD
#coord = [[600,300],[600,700],[1300,300],[1300,700]]  # of the big screen
coord = [[380,190],[900,190],[380,480],[900,480]]  # of ziv's small screen

if what_to_do == "all" or what_to_do.count("aligned") > 0:
    for i in range(loops):
        dir = 'C:\\Users\\ziv98\\Documents\\computer science\\project_haga\\gaze_correction-master\\gaze_correction-master\\gaze_correction_system\\multi_frames'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        if __name__ == '__main__':
            print("starting alignment number " + str(i+1))
            l = mp.Lock()  # multi-process lock
            v = mp.Array('i', [320,240])  # shared parameter
            # start video receiver
            # vs_thread = Thread(target=video_receiver, args=(conf.recver_port,))
            vs_thread = mp.Process(target=regz_socket_MP_FD.video_receiver, args=(v,l))
            vs_thread.start()
            time.sleep(1)
            gz_thread = mp.Process(target=regz_socket_MP_FD.gaze_redirection_system, args=(v,l,coord[i])) # [600,300],[600,700],[1300,300],[1300,700]
            gz_thread.start()
            vs_thread.join()
            gz_thread.join()
            print("finished alignment number " + str(i+1))
            proj_utils.concat(i + 1)
            print("finished concat " + str(i + 1))

if what_to_do == "all" or what_to_do.count("timing") > 0:
    for i in range(loops):
        if __name__ == '__main__':
            proj_utils.look_timing(i)
            # our overlay
            proj_utils.overlay(i)

if what_to_do == "all" or what_to_do.count("compose") > 0:
    if __name__ == '__main__':
        proj_utils.compose()
        # time.sleep(5)
