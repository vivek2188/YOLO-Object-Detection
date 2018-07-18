import numpy as np

def one_hot_encoder(label,label_length):
    # label lies within the range of [0,label_length)
    one_hot_vector = [0] * label_length
    one_hot_vector[label] = 1
    return one_hot_vector

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
