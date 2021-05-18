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

def concat(vid_num):
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


    out = cv2.VideoWriter('aligned_' + str(vid_num) + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

    if vid_num == 2: # when the video is on the "changed" persons's screen
        out_2 = cv2.VideoWriter('aligned_changed.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
        if vid_num == 2:
            out_2.write(img_array[i])

    out.release()
    if vid_num == 2:
        out_2.release()


def compose():

    clip1 = resize(VideoFileClip("final_1.avi"), 0.5)  # add 10px contour
    clip2 = resize(VideoFileClip("final_2.avi"), 0.5)
    clip3 = resize(VideoFileClip("final_3.avi"), 0.5)
    clip4 = resize(VideoFileClip("final_4.avi"), 0.5)
    final_clip = clips_array([[clip1, clip2], [clip3, clip4]])
    final_clip.write_videofile("all_screens.mp4")




names_arr = ["bar's screen", "ziv's screen", "yoni's screen", "orens' screen"]
color_arr = [(0, 0, 255), (0, 255, 0), (204, 153, 255), (200, 200, 0)]
# overlaying the aligned video on the required person + naming the person's screen


def overlay(i):
    print("overlay -> " + str(i+1))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('final_' + str(i + 1) + '.avi', fourcc, 30.0, (1280, 720))

    aligned = cv2.VideoCapture('look_timing_' + str(i + 1) + '.avi')
    zoom = cv2.VideoCapture('ziv-meet.MP4')
    while (aligned.isOpened() and zoom.isOpened()):
        ret, frame = aligned.read()
        ret_zoom, zoom_frame = zoom.read()
        if ret == True and ret_zoom == True:
            # out1.write(frame)
            # frame = cv2.flip(frame,0)
            frame = cv2.resize(frame, (396, 297))
            # zoom_frame[60:357, 642:1168]
            zoom_frame = cv2.putText(zoom_frame, names_arr[i], (400,50), cv2.FONT_HERSHEY_SIMPLEX, 2, color_arr[i], 4, cv2.LINE_AA)

            zoom_frame[60:357, 642:1168] = zoom_frame[60:357, 1167:641:-1]
            zoom_frame[60:357, 707:1103] = frame
            # write the flipped frame
            out.write(zoom_frame)

            # cv2.imshow('frame', frame)

        else:
            break
    out.release()
    aligned.release()
    zoom.release()





# looking at "i" in seconds --- for example [[0,5],[20,27]] means that we are looking at "i" at 0 to 5 seconds and from 20 to 27
# t == top ,,, b == bottom ,,, l == left ,,, r == right
tl_look = [[0,5],[20,27]]
tr_look = [[0,5]]
bl_look = [[0,5]]
br_look = [[0,5]]

# the function applying a straight look only when the person looks at the "i" person, otherwise the look is aligned to the "changed" person.
# that way, when not looking to "i" the gaze is "looking" to the person currently looked at on the screen.
# for example, "i" is on the top left of the screen,the "changed" person is on the top right of the screen, so when looking to the bottom right of the screen,
# the gaze will point downwards instead of regularly pointing bottom right of "changed"

def look_timing(i):
    clip_changed = cv2.VideoCapture("aligned_changed.avi")
    clip_i = cv2.VideoCapture('aligned_' + str(i+1) + '.avi')
    look_arr = [tl_look, tr_look, bl_look, br_look]
    size = (640,480)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('look_timing_' + str(i+1) + '.avi', fourcc, 30.0, size)
    frame_num = 0
    interval = 0  # first interval of the look arrays
    sec = 0
    print ("starting look_timing " + str(i+1))
    while (clip_i.isOpened() and clip_changed.isOpened()):
        ret, frame = clip_i.read()
        ret_changed, changed_frame = clip_changed.read()
        if ret == True and ret_changed == True:
            sec = math.floor(frame_num/30)
            if interval < len(look_arr[i]):
                if sec >= look_arr[i][interval][0] and sec < look_arr[i][interval][1] :
                    frame = cv2.line(frame, (0,479) , (639,479), (0,0,255), 15)
                    frame = cv2.line(frame, (0, 0), (639, 0), (0, 0, 255), 15)
                    out.write(frame)
                    # add here a bottom line --- means that the person is looking straight to you
                elif sec >= look_arr[i][interval][1]:
                    interval += 1
                    out.write(changed_frame)
                else:
                    out.write(changed_frame)
            else:
                out.write(changed_frame)

            frame_num += 1
            # print(str(frame_num) + "   " + str(sec))
        else:
            break
    # print(sec)
    out.release()
    clip_i.release()
    clip_changed.release()

