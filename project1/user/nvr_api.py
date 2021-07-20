from .st import settings
from .nvr_cl import nvr_client
from datetime import datetime
import xmltodict
import re
import json
import os
from urllib.parse import urljoin
import cv2 
import pytesseract

def timeSortKey(e):
  return 60 * e['Hour'] + e['Min']


def response_parser(response, present='dict'):
    """ Convert Hikvision results
    """
    if isinstance(response, (list,)):
        result = "".join(response)
    else:
        result = response.text

    if present == 'dict':
        if isinstance(response, (list,)):
            events = []
            for event in response:
                e = json.loads(json.dumps(xmltodict.parse(event)))
                events.append(e)
            return events
        return json.loads(json.dumps(xmltodict.parse(result)))
    else:
        return result


def getListPlates(date):
    cam = nvr_client(settings.nvr_remote_url, settings.nvr_user, settings.nvr_pass)
    res = cam.getNumberPlates(date, 2)
    res_dict = response_parser(res)["CMSearchResult"]
    list_plate = []
    for i in res_dict["matchList"]["searchMatchItem"]:
        ret = re.search('&name=(.*)&size',
                        i["mediaSegmentDescriptor"]["playbackURI"])
        name = ret.group(1)
        if name.find("unknown") < 0:
            _index = name.rfind("_")
            _len = len(name)
            if _index > 0:
                plate = name[_index + 1:_len:1]
                _time = i["timeSpan"]["startTime"]
                timeD = _time[0:_time.find("T"):1]
                _timeD = datetime.strptime(timeD, "%Y-%m-%d")
                timeH = _time[_time.find("T")+1:len(_time)-1:1]
                _timeH = datetime.strptime(timeH, "%H:%M:%S")
                list_plate.append({"Plate": plate, "Date": _timeD,"Time": _timeH})
                # print("====" + plate + "====" + datetime.strftime(_timeD, '%Y-%m-%d') + "====" + datetime.strftime(_timeH, '%H:%M:%S'))
    return list_plate


def downloadListPlates(date):
    cam = nvr_client(settings.nvr_remote_url, settings.nvr_user, settings.nvr_pass)
    res = cam.getNumberPlates(date, 2)
    res_dict = response_parser(res)["CMSearchResult"]
    
    #create media folder to save data
    media_path = settings.root_path + settings.media_dirname
    if not os.path.exists(media_path):
        os.makedirs(media_path)

    #create media folder to save data
    curdate_path = media_path + datetime.strftime(date, "abc%Yx%mx%d") + "/"
    if not os.path.exists(curdate_path):
        os.makedirs(curdate_path)

    list_plate = []
    for i in res_dict["matchList"]["searchMatchItem"]:
        img_url = i["mediaSegmentDescriptor"]["playbackURI"]
        ret = re.search('&name=(.*)&size', img_url)
        name = ret.group(1)
        if name.find("unknown") < 0:
            _index = name.rfind("_")
            _len = len(name)
            if _index > 0:
                # Download image
                img_path = curdate_path + name + ".jpg"
                if not (os.path.exists(img_path)):
                    cam.download_file(img_url.replace(settings.nvr_local_url,
                                                      settings.nvr_remote_url),
                                      img_path)
                # Get image metadata
                plate = name[_index + 1:_len:1]
                _time = i["timeSpan"]["startTime"]
                timeD = _time[0:_time.find("T"):1]
                # _timeD = datetime.strptime(timeD, "%Y-%m-%d")
                timeH = _time[_time.find("T")+1:len(_time)-1:1]
                # _timeH = datetime.strptime(timeH, "%H:%M:%S")

                # Ignore if the vehicle upward
                img = cv2.imread(img_path)
                crop_img = img[settings.upward_box_y1:settings.upward_box_y2, settings.upward_box_x1:settings.upward_box_x2]
                img_str = pytesseract.image_to_string(crop_img).strip().lower()
                
                vehicle_direction = "unknown"
                if img_str == settings.text_ocr_upward:
                    vehicle_direction = "upward"
                elif img_str == settings.text_ocr_downward:
                    vehicle_direction = "downward"

                print(timeD, timeH, name + ".jpg", vehicle_direction, img_str)

                list_plate.append({"Plate": plate, "Date": timeD,"Time": timeH, "Image": name + ".jpg", "Direction" : vehicle_direction})

    # save json data
    with open(curdate_path + "data.json", 'w+') as f:
        f.write(json.dumps(list_plate, indent=4, sort_keys=True))

    return



