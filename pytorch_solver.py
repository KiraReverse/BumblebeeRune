# from colabcode import ColabCode
from operator import indexOf
from pydoc import classname
from random import random
from click import confirm
from fastapi import FastAPI
# import tensorflow as tf
# physical_devices = tf.config.experimental.list_physical_devices('GPU')
# if len(physical_devices) > 0:
#     tf.config.experimental.set_memory_growth(physical_devices[0], True)
import numpy as np
# cc = ColabCode(port=12000, code=False)
from pydantic import BaseModel
from typing import Optional, List
# from tensorflow.python.saved_model import tag_constants
# from tensorflow.compat.v1 import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession
# import core.utils as utils
import cv2
import datetime
# import sys
from time import perf_counter
# import time
# from PIL import Image, ImageDraw
# from models.tiny_yolo import TinyYoloNet
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet
import torch
import argparse
from collections import OrderedDict
import requests

print(f'hello file')
print(torch.__file__)

"""hyper parameters"""
use_cuda = True

# import socket
# import pickle
# import time
# import select
# from numpy import random
# import cv2
# import json
# import datetime

# import torch
# import torch.backends.cudnn as cudnn
# from models.experimental import attempt_load
# from utils.torch_utils import select_device, load_classifier, time_synchronized
# from utils.general import check_img_size, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, \
#     strip_optimizer, set_logging, increment_path    
# from utils.plots import plot_one_box


class Confirm(BaseModel):
    confirm: bool

class Channel(BaseModel):
    channel: int

class Arrow(BaseModel):
  image: list

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class FLAGSS:
    tiny = False
    model = 'yolov4'

app = FastAPI()

@app.on_event("startup")
def load_model():
    global m
    global class_names
    m = Darknet('yolov4-mish-416.cfg')
    m.print_network()
    m.load_weights('yolov4-mish-416_last.weights')
    print('Loading weights from %s... Done!' % ('yolov4-mish-416_last.weights'))

    if use_cuda:
        m.cuda()
    
    num_classes = m.num_classes
    if num_classes == 20:
        namesfile = 'data/voc.names'
    elif num_classes == 80:
        namesfile = 'data/coco.names'
    else:
        namesfile = 'data/x.names'
    class_names = load_class_names(namesfile)

    global channel
    channel = 30
    global confirmation
    confirmation = True
    print(f'finished loadinng yolov4-mish-416_last.weights ..')
    pass

@app.get("/")
async def read_root():
  print('root')
  return {"message": "hi this is the root"}

@app.post('/predict')
def predict(data: Arrow):
    now=perf_counter()
    global m
    global class_names
    img = np.array(data.image)
    img = img.reshape((228,576,3)).astype('uint8')
    # print(img)
    # print(img.shape)
    # print(len(img))
    # print(type(img))
    # print(type(img[0][0][0]), 'aaaaaaaaaaaa')
    # print(img)

    # save_img0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # date_stamp = str(datetime.datetime.now()).split('.')[0]
    # date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_")
    # file_name = date_stamp + ".jpg"
    # cv2.imwrite('detectpytorch/'+file_name, save_img0)

    sized = cv2.resize(img, (416, 416))
    # print(img.shape)
    for i in range(2):
        start = time.time()
        boxes = do_detect(m, sized, 0.4, 0.6, use_cuda)
        finish = time.time()
        # if i == 1:
        #     print('Predicted in %f seconds.' % ((finish - start)))

    # if len(boxes[0]) != 0:
    #     print(f'boxes: {boxes}')
    #     print(f'boxes2: {boxes[0]}')
    #     print(f'boxes3: {boxes[0][0]}')
    #     print(f'boxes4: {boxes[0][0][0]}')
    # else:
    #     print(f'no detection')
    #     return {'prediction': 'u'}
    xd = {}
    # f = open(f'detectpytorchtxt/{date_stamp}.txt', 'a')
    for b in boxes[0]:
        # print(f'x: {b[0]} c: {b[6]}')
        xd[b[0]] = b[6]
        x1 = b[0] * 576.0
        y1 = b[1] * 228.0
        x2 = b[2] * 576.0
        y2 = b[3] * 228.0
        w = x2 - x1
        h = y2 - y1
        x = (x1+(w/2.0))/576.0
        y = (y1+(h/2.0))/228.0
        w = w / 576.0
        h = h / 228.0
        # x = (b[0]+(b[2]/2.0))/576.0
        # y = (b[1]+(b[3]/2.0))/228.0
        # w = b[2]/576.0
        # h = b[3]/228.0
        # f.write(f'{b[6]} {x} {y} {w} {h}\n') # this
        # f.write(f'{b[6]} {b[0]} {b[1]} {b[2]} {b[3]}\n')
    # print(f'saved detectpytorchtxt/{date_stamp}.txt')
    # f.close()
    sortdict = OrderedDict(sorted(xd.items(), key=lambda x: x[0]))
    alphabets = ''
    for s in sortdict:
        # print(s, sortdict[s])
        if sortdict[s] == 0:
            alphabets += 'u'
        if sortdict[s] == 1:
            alphabets += 'd'
        if sortdict[s] == 2:
            alphabets += 'l'
        if sortdict[s] == 3:
            alphabets += 'r'

    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # plot_boxes_cv2(img, boxes[0], savename='predictions.jpg', class_names=class_names)
  
#   # img = cv2.resize(img, dsize=(640, 640), interpolation=cv2.INTER_CUBIC)
#   img = img / 255.
#   print(img.shape)
#   images_data = []
#   images_data.append(img)
#   images_data = np.asarray(images_data).astype(np.float32)
#   # images_data = img
#   infer = saved_model_loaded.signatures['serving_default']
#   batch_data = tf.constant(images_data)
#   pred_bbox = infer(batch_data)
#   print(f'pred_bbox: {pred_bbox}')
#   for key, value in pred_bbox.items():
#       boxes = value[:, :, 0:4]
#       pred_conf = value[:, :, 4:]
#   boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
#       boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
#       scores=tf.reshape(
#           pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
#       max_output_size_per_class=50,
#       max_total_size=50,
#       iou_threshold=0.45,
#       score_threshold=0.25
#   )
#   pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
#   print(f'pred_bbox: {pred_bbox}')
#   cropped_image = utils.draw_bbox(img, pred_bbox)
#   alphabets = ''
#   for i in range(len(cropped_image)):
#       alphabets += cropped_image[i][1][0]
#       print(cropped_image[i][1])
#   file_name = alphabets + date_stamp + ".jpg"
#   cv2.imwrite('detect/'+file_name, save_img0)
    print(f'{perf_counter()-now=}')
    return {'prediction': alphabets}

@app.post('/sayhi')
def sayhi(data: Arrow):
  print('dummytext')
  print('data: ', data)
  print('data: ', data.image)
  img = np.array(data.image)
  print('data: ', img.shape)
  prediction = model.predict(img)
  class_index = np.argmax(prediction)
  print(class_index)
  print(type(class_index))
  predicted_class = CLASSES[class_index]
  return {"prediction": predicted_class}
  return {"sayhi": 'hi'}
  return data
  return
  
@app.get('/liedetector')
def liedetector():  
  date_stamp = str(datetime.datetime.now()).split('.')[0]
#   date_stamp = date_stamp.replace(" ", "_").replace(":", "_").replace("-", "_")
  print(f'liedetector .. {date_stamp}') 
#   url = 'http://192.168.0.93:3000/notifications' 
#   payload2 = {
#       "title" : "Test Title",
#       "body": "Body of the test push notification",
#       "sound": "default"
#   }
#   r = requests.post(url, json=payload2)

@app.get('/mapleclosed')
def mapleclosed():
  date_stamp = str(datetime.datetime.now()).split('.')[0]
  print(f'maple closed ..{date_stamp}') 
#   url = 'http://192.168.0.93:3000/notifications' 
#   payload2 = {
#       "title" : "Test Title",
#       "body": "Body of the test push notification",
#       "sound": "default"
#   }
#   r = requests.post(url, json=payload2)

@app.get('/characterdied')
def characterdied():
  date_stamp = str(datetime.datetime.now()).split('.')[0]
  print(f'characterdied ..{date_stamp}') 
#   url = 'http://192.168.0.93:3000/notifications' 
#   payload2 = {
#       "title" : "Test Title",
#       "body": "Body of the test push notification",
#       "sound": "default"
#   }
#   r = requests.post(url, json=payload2)

@app.get('/getchannel')
def getchannel():
  print('getchannel ..')
  global channel
  print(channel)
  return {"channel": channel}

@app.post('/setchannel')
def setchannel(data: Channel):
  print('setchannel ..')
  print(f'data: {data}')
  clientchannel = data.channel
  print(data.channel)
  global channel
  print(channel)
  channel = clientchannel
  return {"channel": channel}
  
@app.post('/setconfirm')
def setconfirm(data: Confirm):
    global confirmation
    confirmation = data.confirm
    print(f'confirm: {confirmation}')
    return {"confirm": confirmation}
    pass

@app.get('/getconfirm')
def getconfirm():
    global confirmation
    print(f'confirm: {confirmation}')
    return {"confirm": confirmation}
    pass

@app.get('/changechannel')
def changechannel():
    print('changechannel ..') 
    global channel
    channelr = random.randint(1,30)
    while(channelr == channel):
        channelr = random.randint(1,30)
        pass
    channel = channelr
    return {"channel": channelr}

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.post("/api", tags=["production"])
async def get_predictions():
  try:
    a = 1
  except:
       return {"prediction": "error"}

# cc.run_app(app=app)
# uvicorn captcha_solver:app --host 192.168.0.147 --port 8000
# uvicorn captcha_solver:app --host 192.168.1.95 --port 8000
# uvicorn captcha_solver:app --host 192.168.0.17 --port 8000