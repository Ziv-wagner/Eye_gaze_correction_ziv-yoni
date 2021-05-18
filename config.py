#-*- coding: utf-8 -*-
import argparse

model_config = argparse.ArgumentParser()

# model parameters
model_config.add_argument('--height', type=eval, default=48, help='')
model_config.add_argument('--width', type=eval, default=64, help='')
model_config.add_argument('--channel', type=eval, default=3, help='')
model_config.add_argument('--ef_dim', type=eval, default=12, help='')
model_config.add_argument('--agl_dim', type=eval, default=2, help='')
model_config.add_argument('--encoded_agl_dim', type=eval, default=16, help='')

#demo
model_config.add_argument('--mod', type=str, default="flx", help='')
model_config.add_argument('--weight_set', type=str, default="weights", help='')
model_config.add_argument('--record_time', type=bool, default=False, help='')

model_config.add_argument('--tar_ip', type=str, default='localhost', help='')
#model_config.add_argument('--tar_ip', type=str, default="77.138.155.227", help='')
model_config.add_argument('--sender_port', type=int, default=5005, help='')
model_config.add_argument('--recver_port', type=int, default=5005, help='')
model_config.add_argument('--uid', type=str, default='local', help='')
model_config.add_argument('--P_IDP', type=eval, default=6.1, help='') # 6.8 #
model_config.add_argument('--f', type=eval, default=610, help='') #610  # 345
model_config.add_argument('--P_c_x', type=eval, default=0, help='') #0
model_config.add_argument('--P_c_y', type=eval, default=-14, help='') #-14 # -9
model_config.add_argument('--P_c_z', type=eval, default=-1, help='') #-1
model_config.add_argument('--S_W', type=eval, default=29, help='') #29
model_config.add_argument('--S_H', type=eval, default=17, help='') #17

def get_config():
    config, unparsed = model_config.parse_known_args()
    print(config)
    return config, unparsed
