
# -------- top left person's screen configuration-----
tl_pcx = 0  # distance from screen center to the camera (up is negative) in x-axis
tl_pcy = -9  # distance from screen center to the camera (up is negative) in y-axis
tl_pcz = -1  # distance from screen center to the camera (back is negative) in z-axis
tl_focal = 670  # focal_length
tl_sw = 29  # screen width
tl_sh = 17  # screen height

# -------- top right person's screen configuration-----
tr_pcx = 0  # distance from screen center to the camera (up is negative) in x-axis
tr_pcy = -9  # distance from screen center to the camera (up is negative) in y-axis
tr_pcz = -1  # distance from screen center to the camera (back is negative) in z-axis
tr_focal = 750  # focal_length
tr_sw = 29  # screen width
tr_sh = 17  # screen height

# -------- bottom left person's screen configuration-----
bl_pcx = 0  # distance from screen center to the camera (up is negative) in x-axis
bl_pcy = -11  # distance from screen center to the camera (up is negative) in y-axis
bl_pcz = -1  # distance from screen center to the camera (back is negative) in z-axis
bl_focal = 720  # focal_length
bl_sw = 35  # screen width
bl_sh = 20  # screen height

# -------- bottom right person's screen configuration-----
br_pcx = 0  # distance from screen center to the camera (up is negative) in x-axis
br_pcy = -11  # distance from screen center to the camera (up is negative) in y-axis
br_pcz = -1  # distance from screen center to the camera (back is negative) in z-axis
br_focal = 580  # focal_length
br_sw = 35  # screen width
br_sh = 22  # screen height



#coord = [[600,300],[600,700],[1300,300],[1300,700]]  # of the big screen
#coord = [[380,190],[900,190],[380,480],[900,480]]  # of ziv's small screen
coord_orig = [[380,190],[900,190],[380,480],[900,480]]  # center of each persons image on the "zoom" app window
scr_orient = [[0, 1, 2, 3], [2, 1, 3, 0], [1, 0, 2, 3], [3, 0, 1, 2]]  # the order of the people on each screen (tl,tr,bl,br)



# looking at "i" in seconds --- for example [[0,5],[20,27]] means that we are looking at "i" at 0 to 5 seconds and from 20 to 27
# t == top ,,, b == bottom ,,, l == left ,,, r == right
# ----------------all the look array ------------------------
# for top left
tl_look = [[32,40],[24,25]]
tr_look = [[23,32]]
bl_look = [[7,23],[41,49]]
br_look = [[0,7]]
look_arr_tl = [tl_look, tr_look, bl_look, br_look]
# for top right
tl_look = [[26,35]]
tr_look = [[6,15]]
bl_look = [[0,6],[15,26]]
br_look = [[35,49]]
look_arr_tr = [tl_look, tr_look, bl_look, br_look]
# for bottom left
tl_look = [[15,20],[28,33]]
tr_look = [[44,49]]
bl_look = [[10,15],[21,27],[34,39]]
br_look = [[1,9],[40,43]] #24-25 not very good
look_arr_bl = [tl_look, tr_look, bl_look, br_look]
# for bottom right
tl_look = [[5,14],[20,24]]
tr_look = [[45,49]]
bl_look = [[14,20],[38,45]]
br_look = [[24,37]]
look_arr_br = [tl_look, tr_look, bl_look, br_look]

look_arr_all = [look_arr_tl, look_arr_tr, look_arr_bl, look_arr_br]


# ------------ names of screens and their color
names_arr = ["ziv's screen", "yoni's screen", "irad's screen", "rotem's screen"]
color_arr = [(0, 0, 255), (0, 255, 0), (0, 128, 255), (200, 200, 0)]


def get_proj_config():
    return tl_pcx, tl_pcy, tl_pcz, tl_focal, tl_sw, tl_sh, tr_pcx, tr_pcy, tr_pcz, tr_focal, tr_sw, tr_sh, bl_pcx, bl_pcy, bl_pcz, bl_focal, bl_sw, bl_sh, br_pcx, br_pcy, br_pcz, br_focal, br_sw, br_sh, coord_orig, scr_orient


def get_timing():
    return look_arr_all


def get_name_color():
    return names_arr, color_arr