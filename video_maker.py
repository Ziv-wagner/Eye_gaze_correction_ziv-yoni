import cv2
import sys
import dlib
import time
import socket
import struct
import numpy as np
import tensorflow as tf
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


people = ["tl","tr","bl","br"]  # the real screen participants
people_num = [0,1,2,3]  # the real screen participants in numbers
# loading all configurations
tl_pcx, tl_pcy, tl_pcz, tl_focal, tl_sw, tl_sh, tr_pcx, tr_pcy, tr_pcz, tr_focal, tr_sw, tr_sh, bl_pcx, bl_pcy, bl_pcz, bl_focal, bl_sw, bl_sh, br_pcx, br_pcy, br_pcz, br_focal, br_sw, br_sh, coord_orig, scr_orient = proj_config.get_proj_config()
all_references = []  # will hold later all possible reference points / coordinates that will be used for the gaze correction
ref_oneman = []  # will hold later all possible reference points for single participant at a time

#  find all possible reference points for every participant
for p in people_num:  # all participants
    for s in range(4):  # all screens
        if s == 0:  # for the first screen every participant needs all original reference points
            ref_oneman.append(coord_orig[0])
            ref_oneman.append(coord_orig[1])
            ref_oneman.append(coord_orig[2])
            ref_oneman.append(coord_orig[3])
            continue
        for men in people_num:  # adding the correct reference point for when p looks at men
            p_spot_in_s = coord_orig[scr_orient[s].index(p)]  # position of p inside the screen s
            men_spot_in_s = coord_orig[scr_orient[s].index(men)]  # position of men inside the screen s
            orig_vec = np.subtract(coord_orig[men],coord_orig[p])  # the vector from p to men in the original screen
            new_vec = np.subtract(p_spot_in_s, men_spot_in_s)  # the opposite "new_vec", which is the opposite vector of the vector from p to men in the new screen
            all_vec = np.add(orig_vec, new_vec)  # calculating the final vector which decides on the reference point
            ref_oneman.append(np.add(coord_orig[p],all_vec))  # add the reference point to the collection
    ref_oneman = [tuple(i) for i in ref_oneman]
    ref_oneman = list(set(ref_oneman))
    ref_oneman = [list(i) for i in ref_oneman]  # in these line we "clean" duplications of reference points
    all_references.append(ref_oneman)  # add reference points that belong to participant p
    ref_oneman = []  # clean the array for the next participant

# ---------by now, all_references contains in position "0" all the reference points of men "0", and so on--------



what_to_do = "all"  # decide what will the code do, you can adjust this argument to do any action you want. all - will do all actions, border- only add border to the "zoom" video, and so on....
# just pay attention to the names and where each action is condacted. you can also do several action, example "overlay timing" will do both actions.

# add a border to the "zoom" conference call video.
if what_to_do.count("border") > 0:
    if __name__ == '__main__':
        proj_utils.add_border(VideoFileClip("zoom_vid.mp4"))

# this loop does several operations, that are needed to be done to all participants
for p in people:
    p_index = people.index(p)  # pull the number of the participant, tl is 0, tr is 1, bl is 2, br is 3
    loops = len(all_references[p_index])  # number of loops for the "gaze correction" loop, is determined by the number of reference points.
    coord = all_references[p_index]  # holds all reference points for participant p


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

    # ---------configs for the gaze correction function-----------
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
    # ------------------------------- end of configs ---------------

    # crop the window of participant p from the "zoom" video, so we can align the gaze for p.
    if what_to_do == "all" or what_to_do.count("to_align") > 0:
        if __name__ == '__main__':
            clip = VideoFileClip("zoom_vid_border.mp4")
            proj_utils.crop_to_align(p, clip)

    # here all the gaze correction happens, calling the regz_socket_MP_FD function with all possible reference points.
    # it's a long loop, at the end we will have all videos needed of participant p for the final gaze corrected video.
    if what_to_do == "all" or what_to_do.count("aligned") > 0:
        if __name__ == '__main__':
            clip = VideoFileClip(p + '/to_align.MP4')
            clip.write_videofile('to_align.MP4')
        for i in range(loops):

            if __name__ == '__main__':
                dir = 'C:\\Users\\ziv98\\Documents\\computer science\\project_haga\\gaze_correction-master\\gaze_correction-master\\gaze_correction_system\\multi_frames'
                for f in os.listdir(dir):  # clearing the multi_frames directory
                    os.remove(os.path.join(dir, f))

                # ---------this is how to call the regz_socket_MP_FD-----------
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
                # ---------------------------------------------
                proj_utils.concat(p, i + 1, coord[i])  # concatenate all frames into one continuous video
                print("finished concat " + str(i + 1))

    # timing the video parts so we have the gaze corrected video for each screen
    if what_to_do == "all" or what_to_do.count("timing") > 0:
        if __name__ == '__main__':
            print(p)
            for i in range(4):
                proj_utils.look_timing(p, i, coord_orig, scr_orient[i])  #all_references[p_index]

    #overlaying the gaze corrected video of participant p on the screen of all participants
    if what_to_do == "all" or what_to_do.count("overlay") > 0:
        if __name__ == '__main__':
            print(p)
            for i in range(4):
                proj_utils.overlay(p, i, scr_orient[i])

# compose all screens into one big video of all screens
if what_to_do == "all" or what_to_do.count("compose") > 0:
    if __name__ == '__main__':
        proj_utils.compose()
