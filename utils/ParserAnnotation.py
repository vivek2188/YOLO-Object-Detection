import os
import xml.etree.cElementTree as ET

#annotations_folder = '../datasets/VOC2007/Annotations'
annotations_folder = '../Custom Annotations'

train_xml = [ file for file in sorted(os.listdir(annotations_folder)) ]

# Recursive function
def pretty_printing_xml(root,indentation=0):
    print('    ' * indentation , root.tag , root.text.strip())
    for child in root:
        pretty_printing_xml(child,indentation+1)

def get_bounding_box(obj):
    label = obj.find('name').text.strip()
    bbox = obj.find('bndbox')
    xmin = int(float(bbox.find('xmin').text.strip()))
    ymin = int(float(bbox.find('ymin').text.strip()))
    xmax = int(float(bbox.find('xmax').text.strip()))
    ymax = int(float(bbox.find('ymax').text.strip()))
    return (label,xmin,ymin,xmax,ymax)

def get_img_info(file):
    tree = ET.parse(file)
    root = tree.getroot()
    filename = root.find('filename').text.strip()
    size = root.find('size')
    height = int(size.find('height').text.strip())
    weight = int(size.find('weight').text.strip())
    # Depth always = 3 : RGB
    objects = root.findall('object')
    bndbox = []
    for obj in objects:
        bbox = get_bounding_box(obj)
        bndbox.append(bbox)
    return (filename,height,weight,bndbox)

def get_data():
    train_data = []
    for file in train_xml:
        fl = os.path.join(annotations_folder,file)
        img_info = get_img_info(fl)
        train_data.append(img_info)
    #print(train_data[-1])

    return train_data

if __name__ == '__main__':
    last = os.path.join(annotations_folder,train_xml[-1])
    to_be_parsed = ET.parse(last)
    #print('Annotations: ')
    pretty_printing_xml(to_be_parsed.getroot())
    _ = get_data()
