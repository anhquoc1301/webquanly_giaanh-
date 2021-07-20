from enum import Enum

class settings():
    nvr_local_url = "http://192.168.1.200:80"
    nvr_remote_url = "http://thanhphat-modem.ddns.net"
    nvr_user = "admin"
    nvr_pass = "123456a@"
    root_path = "./"
    media_dirname = "user/media/"
    upward_box_y1 = 1075
    upward_box_y2 = 1140
    upward_box_x1 = 537
    upward_box_x2 = 745             
    text_ocr_upward = "upward"          # using text ocr to detect vehicle direction
    text_ocr_downward = "at re b"       # using text ocr to detect vehicle direction
    text_ocr_unknown = "unknow"         # using text ocr to detect vehicle direction
    vehicle_clear_time = 30             # minutes
