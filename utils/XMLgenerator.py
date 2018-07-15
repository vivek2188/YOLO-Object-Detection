import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET

def write_xml(img_folder,img,objects,tl,br,savedir='Custom Annotations'):
    if not os.path.isdir(savedir):
        os.mkdir(savedir)

    img_name = img.name
    img = cv2.imread(img.path)
    height, weight, depth = img.shape

    annotation = ET.Element('annotation')
    ET.SubElement(annotation,'folder').text = img_folder
    ET.SubElement(annotation,'filename').text = img_name
    ET.SubElement(annotation,'segmented').text = '0'
    size = ET.SubElement(annotation,'size')
    ET.SubElement(size,'height').text = str(height)
    ET.SubElement(size,'weight').text = str(weight)
    ET.SubElement(size,'depth').text = str(depth)

    for obj,tl,br in zip(objects,tl,br):
        ob = ET.SubElement(annotation,'object')
        ET.SubElement(ob,'name').text = obj
        ET.SubElement(ob,'pose').text = 'Unspecified'
        ET.SubElement(ob,'truncated').text = '0'
        ET.SubElement(ob,'difficult').text = '0'
        bnd_box = ET.SubElement(ob,'bndbox')
        ET.SubElement(bnd_box,'xmin').text = str(tl[0])
        ET.SubElement(bnd_box,'ymin').text = str(tl[1])
        ET.SubElement(bnd_box,'xmax').text = str(br[0])
        ET.SubElement(bnd_box,'ymax').text = str(br[1])

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root,pretty_print=True)
    save_path = os.path.join(savedir,img_name.replace('jpg','xml'))
    with open(save_path,'wb') as xmlfile:
        xmlfile.write(xml_str)

if __name__ == '__main__':
    img_folder = '../Custom Images'
    tl = [(10,10)]
    br = [(50,50)]
    obj = ['dog']
    img = None
    for indx,image in enumerate(os.scandir(img_folder)):
        if 'dog_1' in image.name and indx > 0:
            img = image
            break
    write_xml(img_folder,img,obj,tl,br)
