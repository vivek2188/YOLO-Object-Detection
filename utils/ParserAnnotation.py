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

if __name__ == '__main__':
    last = os.path.join(annotations_folder,train_xml[-1])
    to_be_parsed = ET.parse(last)
    pretty_printing_xml(to_be_parsed.getroot())
