import moviepy.editor
import numpy as np
import cv2
#from moviepy.editor import VideoFileClip, concatenate_videoclips

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('fibruk_2.avi',fourcc, 20.0, (640,480))
# out1 = cv2.VideoWriter('out1.avi',fourcc, 5.0, (640,480))
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # out1.write(frame)
        # frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished

# out = out.fx(moviepy.editor.vfx.speedx, 0.01)
# out1 = out1.fx(moviepy.editor.vfx.speedx, 3)
cap.release()
out.release()
# out1.release()
cv2.destroyAllWindows()