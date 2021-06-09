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


people = ["tl","tr","bl","br"]
noam_pcy = -10
noam_focal = 920
yoni_pcy = -9
yoni_focal = 880
ziv_pcy = -9
ziv_focal = 920
bar_pcy = -19
bar_focal = 750




loops = 4
what_to_do = " timing compose"

for p in people:

    conf,_ = get_config()
    # set config to each participant
    if p == "tl":
        conf.P_c_y = noam_pcy
        conf.f = noam_focal
    if p == "tr":
        conf.P_c_y = yoni_pcy
        conf.f = yoni_focal
    if p == "bl":
        conf.P_c_y = bar_pcy
        conf.f = bar_focal
        conf.S_W = 51
        conf.S_H = 30
    if p == "br":
        conf.P_c_y = ziv_pcy
        conf.f = ziv_focal

    if conf.mod == 'flx':
        import flx as model
    else:
        sys.exit("Wrong Model selection: flx or deepwarp")

    # system parameters
    model_dir = './'+conf.weight_set+'/warping_model/'+conf.mod+'/'+ str(conf.ef_dim) + '/'
    size_video = [640,480]
    # fps = 0
    P_IDP = 5
    depth = -50
    # for monitoring
    # environment parameter
    Rs = (GetSystemMetrics(0),GetSystemMetrics(1))
    # In[ ]:
    model_dir
    print(Rs)





    if what_to_do == "all" or what_to_do.count("to_align") > 0:
        if __name__ == '__main__':
            clip = VideoFileClip("yoni-meet-25-border.mp4")
            proj_utils.crop_to_align(p, clip)
            # newClip = crop(clip, x_center=x_center_tr, y_center=y_center_tr, width=height_tr*(4/3), height=height_tr)
            # newClip = newClip.resize((640,480))
            # newClip.write_videofile('to_aline.MP4')

    # this is how to call the regz_socket_MP_FD
    #coord = [[600,300],[600,700],[1300,300],[1300,700]]  # of the big screen
    coord = [[380,190],[900,190],[380,480],[900,480]]  # of ziv's small screen

    if what_to_do == "all" or what_to_do.count("aligned") > 0:
        if __name__ == '__main__':
            clip = VideoFileClip(p + '/to_aline.MP4')
            clip.write_videofile('to_aline.MP4')
        for i in range(loops):

            if __name__ == '__main__':
                dir = 'C:\\Users\\ziv98\\Documents\\computer science\\project_haga\\gaze_correction-master\\gaze_correction-master\\gaze_correction_system\\multi_frames'
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))

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
                proj_utils.concat(p, i + 1)
                print("finished concat " + str(i + 1))

    if what_to_do == "all" or what_to_do.count("timing") > 0:
        if __name__ == '__main__':
            print(p)
            for i in range(loops):
                proj_utils.look_timing(p, i)
                # our overlay
                proj_utils.overlay(p, i)

if what_to_do == "all" or what_to_do.count("compose") > 0:
    if __name__ == '__main__':
        proj_utils.compose()
        # time.sleep(5)
