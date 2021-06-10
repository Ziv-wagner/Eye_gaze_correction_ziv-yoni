# from moviepy.editor import concatenate_videoclips, VideoFileClip
# import cv2
# vid2=VideoFileClip("test.avi")
# vid1=VideoFileClip("out1.avi")
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # tester = cv2.VideoWriter('test.avi',fourcc, 5.0, (640,480))
# # cap = cv2.VideoCapture(0)
# # ret, frame = cap.read()
# # cap.release()
# # tester.write(frame)
# # tester.release()
# vid=VideoFileClip("test.avi")
# vid.write_videofile('try_1.mp4')
# # final_video= concatenate_videoclips([vid1, vid])
# # final_video.write_videofile('final_video.mp4')
# # print(int(vid.duration()))


import cv2
import numpy as np
import math
import glob
from natsort import natsorted
from moviepy.editor import VideoFileClip, clips_array, vfx
from moviepy.video.fx.resize import resize
from moviepy.video.fx.crop import crop

import proj_utils


def concat(p, vid_num, coord):
    img_array = []
    glob_res = glob.glob('C:\\Users\\ziv98\\Documents\\computer science\\project_haga\\gaze_correction-master\\gaze_correction-master\\gaze_correction_system\\multi_frames\\*.jpg')
    glob_res = natsorted(glob_res)
    # print(glob_res)
    size = (640,480)
    for filename in glob_res:
        img = cv2.imread(filename)
        # print(filename)
        img = cv2.flip(img, 1)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)


    out = cv2.VideoWriter(p + '/aligned_' + str(coord) + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    a = people.index(p)
    changed = a + 1
    if vid_num == changed: # when the video is on the "changed" persons's screen
        out_2 = cv2.VideoWriter(p + '/aligned_changed.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
        if vid_num == changed:
            out_2.write(img_array[i])

    out.release()
    if vid_num == changed:
        out_2.release()


def compose():

    clip1 = resize(VideoFileClip("tl/final_3.avi"), 0.5)  # add 10px contour
    clip2 = resize(VideoFileClip("tr/final_3.avi"), 0.5)
    clip3 = resize(VideoFileClip("bl/final_3.avi"), 0.5)
    clip4 = resize(VideoFileClip("br/final_3.avi"), 0.5)
    final_clip = clips_array([[clip1, clip2], [clip3, clip4]])
    final_clip.write_videofile("all_screens.mp4")





# looking at "i" in seconds --- for example [[0,5],[20,27]] means that we are looking at "i" at 0 to 5 seconds and from 20 to 27
# t == top ,,, b == bottom ,,, l == left ,,, r == right
# for noam
# all the look array
tl_look = [[12,17],[24,25]]
tr_look = []
bl_look = [[7,12],[17,24]]
br_look = [[3,7]]
look_arr_tl = [tl_look, tr_look, bl_look, br_look]
# for yoni
tl_look = [[17,24]]
tr_look = [[5,12]]
bl_look = [[0,5],[12,17]]
br_look = [[24,25]]
look_arr_tr = [tl_look, tr_look, bl_look, br_look]
# for bar
tl_look = [[6,12],[17,24]]
tr_look = [[0,6]]
bl_look = [[12,17]]
br_look = [[24,25]] #24-25 not very good
look_arr_bl = [tl_look, tr_look, bl_look, br_look]
# for ziv
tl_look = [[24,25]]
tr_look = [[16,24]]
bl_look = [[6,16]]
br_look = [[0,6]]
look_arr_br = [tl_look, tr_look, bl_look, br_look]

look_arr_all = [look_arr_tl, look_arr_tr, look_arr_bl, look_arr_br]


names_arr = ["noam's screen", "yoni's screen", "bar's screen", "ziv's screen"]
color_arr = [(0, 0, 255), (0, 255, 0), (204, 153, 255), (200, 200, 0)]
# overlaying the aligned video on the required person + naming the person's screen


people = ["tl","tr","bl","br"]

def overlay(p, i, scr_orient):
    a = people.index(p)
    p_spot_in_i = scr_orient.index(a)
    orig_coord, stam1, stam2 = proj_utils.get_coordinates(a)
    orig_coord = orig_coord[0]
    coord, width, height = proj_utils.get_coordinates(p_spot_in_i)
    x_center = math.floor((coord[0][0] + coord[1][0]) / 2)
    y_center = math.floor((coord[0][1] + coord[1][1]) / 2)
    tl_coord = coord[0]
    print("overlay -> " + str(i+1))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    a = people.index(p)

    if i == 0:
        out = cv2.VideoWriter("tl" + '/final_' + str(a) + '.avi', fourcc, 30.0, (1400, 840))
    if i == 1:
        out = cv2.VideoWriter("tr" + '/final_' + str(a) + '.avi', fourcc, 30.0, (1400, 840))
    if i == 2:
        out = cv2.VideoWriter("bl" + '/final_' + str(a) + '.avi', fourcc, 30.0, (1400, 840))
    if i == 3:
        out = cv2.VideoWriter("br" + '/final_' + str(a) + '.avi', fourcc, 30.0, (1400, 840))

    if p == "tl":
        zoom = cv2.VideoCapture('yoni-meet-25-border.mp4')
    else:
        if i == 0:
            zoom = cv2.VideoCapture("tl" + '/final_' + str(a-1) + '.avi')
        if i == 1:
            zoom = cv2.VideoCapture("tr" + '/final_' + str(a-1) + '.avi')
        if i == 2:
            zoom = cv2.VideoCapture("bl" + '/final_' + str(a-1) + '.avi')
        if i == 3:
            zoom = cv2.VideoCapture("br" + '/final_' + str(a-1) + '.avi')
    # out = cv2.VideoWriter('final_' + str(i + 1) + '.avi', fourcc, 30.0, (1400, 840))
    # x_center = math.floor(tl_coord[0] + width/2)
    # y_center = math.floor(tl_coord[1] + height/2)

    orig_zoom = cv2.VideoCapture('yoni-meet-25-border.mp4')
    aligned = cv2.VideoCapture(p + '/look_timing_' + str(i + 1) + '.avi')
    # zoom = cv2.VideoCapture('yoni-meet-25-border.mp4')

    # --------- here it's all for the square when looking-------
    look_arr = look_arr_all[a]
    frame_num = 0
    interval = 0  # first interval of the look arrays
    sec = 0
    #------------------
    while aligned.isOpened() and zoom.isOpened():
        ret, frame = aligned.read()
        ret_zoom, zoom_frame = zoom.read()
        ret_orig, orig_frame = orig_zoom.read()

        if ret == True and ret_zoom == True and ret_orig == True:
            # out1.write(frame)
            # frame = cv2.flip(frame,0)
            frame = cv2.resize(frame, (math.floor(height*(4/3)), height))
            # zoom_frame[60:357, 642:1168]
            zoom_frame = cv2.putText(zoom_frame, names_arr[i], (460,50), cv2.FONT_HERSHEY_SIMPLEX, 2, color_arr[i], 4, cv2.LINE_AA)

            zoom_frame[tl_coord[1]:tl_coord[1] + height, tl_coord[0]:tl_coord[0] + width] = orig_frame[orig_coord[1]:orig_coord[1] + height, orig_coord[0] + width - 1:orig_coord[0] - 1:-1]
            zoom_frame[tl_coord[1]:tl_coord[1] + height, x_center - math.floor(height*(2/3)):x_center + math.floor(height*(2/3))] = frame

            # --------- here it's all for the square when looking-------
            sec = math.floor(frame_num / 30)


            if interval < len(look_arr[i]):
                if look_arr[i][interval][0] <= sec < look_arr[i][interval][1]:
                    thick = 4
                    zoom_frame = cv2.line(zoom_frame, (coord[0][0] + thick, coord[0][1] + thick), (coord[1][0] - thick, coord[0][1] + thick), color_arr[a], thick*2)  # top line
                    zoom_frame = cv2.line(zoom_frame, (coord[0][0] + thick, coord[1][1] - thick), (coord[1][0] - thick, coord[1][1] - thick), color_arr[a], thick*2)  # bottom line
                    zoom_frame = cv2.line(zoom_frame, (coord[0][0] + thick, coord[0][1] + thick), (coord[0][0] + thick, coord[1][1] - thick), color_arr[a], thick*2)  # left line
                    zoom_frame = cv2.line(zoom_frame, (coord[1][0] - thick, coord[0][1] + thick), (coord[1][0] - thick, coord[1][1] - thick), color_arr[a], thick*2)  # right line
                    # add here a bottom line --- means that the person is looking straight to you
                elif sec >= look_arr[i][interval][1]:
                    interval += 1
            frame_num += 1
            # --------------------------------------------------------
            # write the flipped frame
            out.write(zoom_frame)

            # cv2.imshow('frame', frame)

        else:
            break
    out.release()
    aligned.release()
    zoom.release()
    orig_zoom.release()


# the function applying a straight look only when the person looks at the "i" person, otherwise the look is aligned to the "changed" person.
# that way, when not looking to "i" the gaze is "looking" to the person currently looked at on the screen.
# for example, "i" is on the top left of the screen,the "changed" person is on the top right of the screen, so when looking to the bottom right of the screen,
# the gaze will point downwards instead of regularly pointing bottom right of "changed"
# p is the changed person, i is the screen owner
def look_timing(p, i, coord, scr_orient):
    a = people.index(p)
    ref_points = []
    for men in range(4):
        p_spot_in_i = coord[scr_orient.index(a)]
        men_spot_in_i = coord[scr_orient.index(men)]
        orig_vec = np.subtract(coord[men], coord[a])
        new_vec = np.subtract(p_spot_in_i, men_spot_in_i)  # the opposite "new_vec"
        all_vec = np.add(orig_vec, new_vec)
        wanted_coord = np.add(coord[a], all_vec)
        ref_points.append(wanted_coord)
    print("p=" + str(p) + " , i=" + str(i) + " , orient= " + str(scr_orient) + " , ref_points = " + str(ref_points))
    owner_clip = cv2.VideoCapture(p + "/aligned_" + str(coord[i]) + ".avi")
    tl_clip = cv2.VideoCapture(p + "/aligned_" + str(ref_points[0].tolist()) + ".avi")
    tr_clip = cv2.VideoCapture(p + "/aligned_" + str(ref_points[1].tolist()) + ".avi")
    bl_clip = cv2.VideoCapture(p + "/aligned_" + str(ref_points[2].tolist()) + ".avi")
    br_clip = cv2.VideoCapture(p + "/aligned_" + str(ref_points[3].tolist()) + ".avi")
    look_arr = look_arr_all[a]
    # look_arr = [tl_look, tr_look, bl_look, br_look]
    size = (640,480)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(p + '/look_timing_' + str(i+1) + '.avi', fourcc, 30.0, size)
    frame_num = 0
    interval = 0  # first interval of the look arrays
    sec = 0
    print ("starting look_timing " + str(i+1))
    while tl_clip.isOpened() and tr_clip.isOpened() and bl_clip.isOpened() and br_clip.isOpened() and owner_clip.isOpened():
        tl_ret, tl_frame = tl_clip.read()
        tr_ret, tr_frame = tr_clip.read()
        bl_ret, bl_frame = bl_clip.read()
        br_ret, br_frame = br_clip.read()
        owner_ret, owner_frame = owner_clip.read()

        if tl_ret == True and tr_ret == True and bl_ret == True and br_ret == True and owner_ret == True:
            sec = math.floor(frame_num/30)
            # if sec == 2 and a == 1:
            #     stop = 0
            # finding the men we are looking at at this second
            finito = 0
            look_at = a
            for u in range(len(look_arr)):
                for j in range(len(look_arr[u])):
                    if look_arr[u][j][0] <= sec < look_arr[u][j][1]:
                        finito = 1
                        look_at = u
                        break
                if finito == 1:
                    break
            # if finito == 0:
            #     print("wtf is this and time = " + str(sec))
            if look_at == i:
                out.write(owner_frame)
            elif look_at == 0:
                out.write(tl_frame)
            elif look_at == 1:
                out.write(tr_frame)
            elif look_at == 2:
                out.write(bl_frame)
            elif look_at == 3:
                out.write(br_frame)
            else:
                out.write(tl_frame)
                print("wtf is this and time = " + str(sec))  # shouldnt happen

            # if interval < len(look_arr[i]):
            #     if sec >= look_arr[i][interval][0] and sec < look_arr[i][interval][1] :
            #         # frame = cv2.line(frame, (0,479) , (639,479), color_arr[a], 15)
            #         # frame = cv2.line(frame, (0, 0), (639, 0), color_arr[a], 15)
            #         out.write(frame)
            #         # add here a bottom line --- means that the person is looking straight to you
            #     elif sec >= look_arr[i][interval][1]:
            #         interval += 1
            #         out.write(changed_frame)
            #     else:
            #         out.write(changed_frame)
            # else:
            #     out.write(changed_frame)

            frame_num += 1
            # print(str(frame_num) + "   " + str(sec))
        else:
            break
    # print(sec)
    out.release()
    tl_clip.release()
    tr_clip.release()
    bl_clip.release()
    br_clip.release()
    owner_clip.release()


# ----------crop zoom video to a single man video----------#
    #all video - (top left = (60,60), bottom right = (1340,780))
    # tr = [[700, 60], [1340, 420]]
    # x_center_tr = math.floor((tr[0][0] + tr[1][0])/2)
    # y_center_tr = math.floor((tr[0][1] + tr[1][1])/2)
    # height_tr = math.floor(tr[1][1] - tr[0][1])
    # width_tr = math.floor(tr[1][0] - tr[0][0])
#     tl = [[60, 60], [700, 420]]
#     tr = [[700, 60], [1340, 420]]
#     bl = [[60,420], [700,780]]
#     br = [[700,420], [1340,780]]
    # top right = x_center=905 , y_center=209, width=528, height=299
def crop_to_align(p, clip):
    a = people.index(p)
    coord, Width, Height = proj_utils.get_coordinates(a)
    xCenter = math.floor((coord[0][0] + coord[1][0]) / 2)
    yCenter = math.floor((coord[0][1] + coord[1][1]) / 2)
    newClip = crop(clip, x_center=xCenter, y_center=yCenter, width=Height * (4 / 3), height=Height)
    newClip = newClip.resize((640, 480))
    newClip.write_videofile(p + '/to_aline.MP4')
    newClip.write_videofile('to_aline.MP4')




def get_coordinates(p):
    # coord first argument is top left coord of the wanted screen area , second argument is the bottom right coord
    if p == 0:
        coord = [[60, 60], [700, 420]]
    if p == 1:
        coord = [[700, 60], [1340, 420]]
    if p == 2:
        coord = [[60, 420], [700, 780]]
    if p == 3:
        coord = [[700, 420], [1340, 780]]
    xCenter = math.floor((coord[0][0] + coord[1][0]) / 2)
    yCenter = math.floor((coord[0][1] + coord[1][1]) / 2)
    height = math.floor(coord[1][1] - coord[0][1])
    width = math.floor(coord[1][0] - coord[0][0])
    return coord, width, height