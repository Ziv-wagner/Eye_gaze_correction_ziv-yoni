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
import itertools
from moviepy.editor import concatenate_videoclips, VideoFileClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize

import regz_socket_MP_FD
import proj_utils
import proj_config
# regz_socket_MP_FD#.regz([600,300])


people = ["tl","tr","bl","br"]  # the real screen
people_num = [0,1,2,3]
tl_pcx, tl_pcy, tl_pcz, tl_focal, tl_sw, tl_sh, tr_pcx, tr_pcy, tr_pcz, tr_focal, tr_sw, tr_sh, bl_pcx, bl_pcy, bl_pcz, bl_focal, bl_sw, bl_sh, br_pcx, br_pcy, br_pcz, br_focal, br_sw, br_sh, coord_orig, scr_orient = proj_config.get_proj_config()
all_references = []
ref_oneman = []

for p in people_num:
    for s in range(4):  # all screens
        if s == 0:
            ref_oneman.append(coord_orig[0])
            ref_oneman.append(coord_orig[1])
            ref_oneman.append(coord_orig[2])
            ref_oneman.append(coord_orig[3])
            continue
        for men in people_num:
            p_spot_in_s = coord_orig[scr_orient[s].index(p)]
            men_spot_in_s = coord_orig[scr_orient[s].index(men)]
            orig_vec = np.subtract(coord_orig[men],coord_orig[p])
            new_vec = np.subtract(p_spot_in_s, men_spot_in_s)  #the opposite "new_vec"
            all_vec = np.add(orig_vec, new_vec)
            ref_oneman.append(np.add(coord_orig[p],all_vec))
    ref_oneman = [tuple(i) for i in ref_oneman]
    ref_oneman = list(set(ref_oneman))
    ref_oneman = [list(i) for i in ref_oneman]
    all_references.append(ref_oneman)
    ref_oneman = []

# ---------by now, all_references contains in 0 all the references of men 0, and so on--------


# loops = 1
what_to_do = "all"

if what_to_do.count("border") > 0:
    if __name__ == '__main__':
        proj_utils.add_border(VideoFileClip("zoom_vid.mp4"))

for p in people:
    p_index = people.index(p)
    loops = len(all_references[p_index])
    coord = all_references[p_index]


    conf,_ = get_config()
    # set config to each participant
    if p == "tl":
        conf.P_c_y = tl_pcy
        conf.f = tl_focal
        conf.S_W = tl_sw
        conf.S_H = tl_sh
    if p == "tr":
        conf.P_c_y = tr_pcy
        conf.f = tr_focal
        conf.S_W = tr_sw
        conf.S_H = tr_sh
    if p == "bl":
        conf.P_c_y = bl_pcy
        conf.f = bl_focal
        conf.S_W = bl_sw
        conf.S_H = bl_sh
    if p == "br":
        conf.P_c_y = br_pcy
        conf.f = br_focal
        conf.S_W = br_sw
        conf.S_H = br_sh

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
            clip = VideoFileClip("zoom_vid_border.mp4")
            proj_utils.crop_to_align(p, clip)

            # newClip = crop(clip, x_center=x_center_tr, y_center=y_center_tr, width=height_tr*(4/3), height=height_tr)
            # newClip = newClip.resize((640,480))
            # newClip.write_videofile('to_aline.MP4')

    # this is how to call the regz_socket_MP_FD


    if what_to_do == "all" or what_to_do.count("aligned") > 0:
        if __name__ == '__main__':
            clip = VideoFileClip(p + '/to_align.MP4')
            clip.write_videofile('to_align.MP4')
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
                proj_utils.concat(p, i + 1, coord[i])
                print("finished concat " + str(i + 1))

    if what_to_do == "all" or what_to_do.count("timing") > 0:
        if __name__ == '__main__':
            print(p)
            # loops = len(all_references[p])

            for i in range(4):
                proj_utils.look_timing(p, i, coord_orig, scr_orient[i])  #all_references[p_index]

    if what_to_do == "all" or what_to_do.count("overlay") > 0:
        if __name__ == '__main__':
            print(p)
            for i in range(4):
                # our overlay
                proj_utils.overlay(p, i, scr_orient[i])

if what_to_do == "all" or what_to_do.count("compose") > 0:
    if __name__ == '__main__':
        proj_utils.compose()
        # time.sleep(5)
