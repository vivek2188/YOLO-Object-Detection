import os
import numpy as np
import xml.etree.cElementTree as ET

#annotations_folder = '../datasets/VOC2007/Annotations'
#annotations_folder = '../Custom Annotations'

#train_xml = [ file for file in sorted(os.listdir(annotations_folder)) ]

def labels_dict(labels):
    labels_length = len(labels)
    return dict(zip(sorted(labels),np.arange(0,labels_length)))

def convert_minmax_to_wh(xmin,ymin,xmax,ymax):
    c_x = (xmin + xmax) / 2.0
    c_y = (ymin + ymax) / 2.0
    w = xmax - xmin
    h = ymax - ymin
    return (c_x, c_y, w, h)

# Recursive function
def pretty_printing_xml(root,indentation=0):
    print('    ' * indentation , root.tag , root.text.strip())
    for child in root:
        pretty_printing_xml(child,indentation+1)

def get_bounding_box(obj,lbls_dict):
    label_v = obj.find('name').text.strip()
    label = lbls_dict[label_v]
    bbox = obj.find('bndbox')
    # Bounding box values from the Annotation
    xmin = float(bbox.find('xmin').text.strip())
    ymin = float(bbox.find('ymin').text.strip())
    xmax = float(bbox.find('xmax').text.strip())
    ymax = float(bbox.find('ymax').text.strip())
    # But we want the values of the bounding box to be Center Coordinates and Width and Height of the box.
    center_x, center_y, width, height = convert_minmax_to_wh(xmin,ymin,xmax,ymax)
    return (label,center_x,center_y,width,height)

def get_img_info(file,lbls_dict):
    tree = ET.parse(file)
    root = tree.getroot()
    filename = root.find('filename').text.strip()
    size = root.find('size')
    height = int(size.find('height').text.strip())
    width = int(size.find('width').text.strip())
    # Depth always = 3 : RGB
    objects = root.findall('object')
    bndbox = []
    for obj in objects:
        bbox = get_bounding_box(obj,lbls_dict)
        bndbox.append(bbox)
    return (filename,height,width,bndbox)

def get_data(annotations_folder,labels):
    '''
    Output for each file will be:
        [filename, width, height, bounding boxes]
    '''
    lbls_dict = labels_dict(labels)
    train_xml = [ file for file in sorted(os.listdir(annotations_folder)) ]
    train_data = []
    for file in train_xml:
        fl = os.path.join(annotations_folder,file)
        img_info = get_img_info(fl,lbls_dict)
        train_data.append(img_info)
    return (train_xml, train_data)

if __name__ == '__main__':
    last = os.path.join(annotations_folder,train_xml[-1])
    to_be_parsed = ET.parse(last)
    #print('Annotations: ')
    pretty_printing_xml(to_be_parsed.getroot())
