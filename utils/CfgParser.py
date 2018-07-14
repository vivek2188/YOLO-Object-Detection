#-----------HELPER FUNCTION-----------------

# yolov2-tiny.cfg
# net -- convolutional -- maxpool -- region
# yolov2.cfg
# net -- convolutional -- maxpool -- route -- reorg -- region
# yolov3-tiny.cfg
# net -- convolutional -- maxpool -- upsample -- route -- yolo
#yolov3.cfg
# net -- convolutional -- maxpool -- shortcut -- upsample -- route -- yolo

def cfg_parser(cfg_file):
    #Opening the cfg file
    file = open(cfg_file,'r')
    #Reading the contents of the file
    content = file.read()
    lines = []
    for data in content.split('\n'):
        if len(data) > 0:
            if data[0] != '#':
                #Removing white spaces from both sides
                data = data.lstrip().rstrip()
                lines.append(data)
    # There are different blocks present in the cfg file
    # Like: net, convolutional, maxpool, upsample etc.
    # Store each of these blocks and return them.
    blocks = list()
    block = dict()
    for line in lines:
        if line[0] == '[':
            #Check whether the last block has been appended
            if len(block) != 0:
                blocks.append(block)
                block = {}
            block['type'] = line[1:-1].rstrip()
        else:
            key, value = line.split('=')
            block[key.rstrip()] = value.lstrip()
    blocks.append(block)
    print(len(blocks))
    return blocks

if __name__ == '__main__':
    cfg_parser('./../cfg/yolov3-tiny.cfg')
