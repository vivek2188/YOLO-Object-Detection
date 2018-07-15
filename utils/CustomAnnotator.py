import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from XMLgenerator import write_xml

# Global Variable
topLeftCoords = list()
bottomRightCoords = list()
object_list = list()

# Constants
img = None
img_folder = '../Custom Images'
annotations = '../Custom Annotations'
obj = 'dogs'

def line_select_callback(click,release):
    global topLeftCoords
    global bottomRightCoords
    global object_list

    object_list.append(obj)
    topLeftCoords.append((click.xdata,click.ydata))
    bottomRightCoords.append((release.xdata,release.ydata))


def toggleSelector(event):
    toggleSelector.RS.set_active(True)

def onkeypress(event):
    global topLeftCoords
    global bottomRightCoords
    global object_list
    global img

    if event.key == 'q':
        write_xml(img_folder,image,object_list,topLeftCoords,bottomRightCoords,savedir=annotations)
        topLeftCoords = []
        bottomRightCoords = []
        object_list = []
        img = None
        plt.close()

if __name__ == '__main__':
    print('-------------Running Custom Annotator-----------------')

    for indx, image in enumerate(os.scandir(img_folder)):
        if indx:        # So that it does not consider .ipynb checkpoint file
            img = image
            img_path = image.path
            img_name = img.name
            fig, ax = plt.subplots(1)
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            ax.imshow(img)

            toggleSelector.RS = RectangleSelector(
                ax,line_select_callback,
                drawtype='box',useblit=True,
                minspanx=5,minspany=5,
                spancoords='pixels',
                interactive=True
            )
            bnd_box = plt.connect('key_press_event',toggleSelector)
            key = plt.connect('key_press_event',onkeypress)
            plt.show()

# With the use of FOR loop we can automate the process of annotation generation over the various opbjects.
