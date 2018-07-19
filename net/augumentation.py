# Preparing the TARGET VARIABLES
import os
import cv2
import sys
import numpy as np
from PIL import Image
from PIL import ImageDraw
import matplotlib.pyplot as plt

sys.path.append('C:\\Users\\user\\YOLO-Object-Detection')
from utils.ParserAnnotation import get_data

def resize(image,img_size):
    img = cv2.imread(image.path)
    img = cv2.cvtColor(img,cv2.COL0R_BGR2RGB)
    h,w, _ = img.shape
    if h*w < 416*416:
        interpolation = cv2.INTER_LINEAR
    else:
        interpolation = cv2.INTER_AREA
    img = cv2.resize(img,dsize=(img_size,img_size),interpolation=interpolation)
    return img

def one_hot_encoder(label,label_length):
    # label lies within the range of [0,label_length)
    one_hot_vector = [0] * label_length
    one_hot_vector[label] = 1
    return one_hot_vector

def draw_rectangles(obj,rect_coords,line_width=1,color='red'):
    # rect_coords = (X,Y)
    coords = (rect_coords[0][0],rect_coords[0][1],rect_coords[1][0],rect_coords[1][1])
    for i in range(line_width):
        obj.rectangle(coords,outline=color)
        coords = (coords[0]+1,coords[1]+1,coords[2]+1,coords[3]+1)

def convert_to_yolo(label,img_height,img_width,grid_size,n_classes):
    '''
    After parsing the annotations, we get the output of the following format:
         [img_name,height,width,[object1,object2,....,objectN]] per annotation assuming there are N objects to recognise.
    where each objectI = [center_x,center_y,width,height,ONE_HOT_VECTOR]

    In YOLO Algorithm, we divide the image into the grid for size say n.
    For detecting whether our model is predicting correctly Output should be of the shape of (m, grid_size, grid_size, 5+n_classes)
    5 represents : objectness score (0 or 1) , X, Y, W, H
    m = Number of the samples.
    This function helps in acheiving this goal.
    '''
    output = np.zeros((1,grid_size,grid_size,5+n_classes))

    n_obj = label.shape[1]
    for obj in range(n_obj):
        one_hot_vector = label[obj,4:]
        if np.all(one_hot_vector==0):
            continue
        # Bounding box parameters
        X = label[obj,0]
        Y = label[obj,1]
        W = label[obj,2]
        H = label[obj,3]
        # Transformed parameters
        trans_X = (X / img_width) * grid_size
        trans_Y = (Y / img_height) * grid_size
        trans_W = W / img_width
        trans_H = H / img_height
        # X Modulo 1 : we want our center to be within the range of [0,1] because their is position is relative to the pixel in which its present rather than the whole grid
        output[0,int(trans_Y),int(trans_X)] = np.concatenate([1,trans_X%1,trans_Y%1,trans_W,trans_H],one_hot_vector)
    return output

def transform_labels(labels,img_height,img_width,grid_size,n_classes):
    yolo_output = []
    for label in labels:
        yolo_output.append(convert_to_yolo(label,img_height,img_width,grid_size,n_classes))
    return yolo_output

def create_distributor(annotations_folder,labels):
    label_data = []
    img_path_list = []
    label_list = []
    file_list, dataset = get_data(annotations_folder,labels)
    return file_list[:3]
