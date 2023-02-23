import cv2 as cv
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



'''
command is a list of command, it is a tuple, first is command, second is variable. 
stack is a list of value
'''
#Image Binary class
class ImBin:
    def __init__(self,data:bytes,format):
        self.data=data
        self.format=format

def add(stack,username,cache):
    stack.append(stack.pop()+stack.pop())
    return
def substract(stack,username,cache):
    stack.append(stack.pop()-stack.pop())
    return
def multiply(stack,username,cache):
    stack.append(stack.pop()*stack.pop())
    return
def invertIm(stack,username,cache):
    img=stack.pop()
    channel=getChannel(img)
    if channel==3 or channel==1:
        img=(255-img)
        stack.append(img)
    elif channel==4:
        img[:,:,0:3]=255-img[:,:,0:3]
        stack.append(img)
def blur(stack,username,cache):
    print("blur")
    img=stack.pop()
    stack.append(cv.blur(img,(5,5)))
# convert numpy image to bytes and package to ImBin object
def toIm(stack,username,cache):
    array=stack.pop()
    c=getChannel(array)
    if c==1 or c==3:
        encode=".jpg"
    else:
        encode=".png"
    imgByteArr = cv.imencode(encode, array)[1].tobytes()
    stack.append(ImBin(imgByteArr,encode))
    return
def linspace(stack,username,cache):
    p1=stack.pop()
    p2=stack.pop()
    stack.append(np.linspace(p1, p2, 200))
    return
def sin(stack,username,cache):
    stack.append(np.sin(stack.pop()/180*np.pi))
    return
def cos(stack,username,cache):
    stack.append(np.cos(stack.pop()/180*np.pi))
    return
def plot(stack,username,cache):
    fig=Figure()
    canvas=FigureCanvas(fig)
    ax= fig.gca()
    x = stack.pop()
    y = stack.pop()
    ax.plot(x, y)
    #fig.tight_layout(pad=0)
    #ax.margins(0)
    fig.canvas.draw()
    image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    stack.append(image_from_plot)

def getChannel(img):
    if len(img.shape)==2:
        return 1
    else:
        return img.shape[-1]
#init function library

funlibrary={}
funlibrary['add']=add
funlibrary['substract']=substract
funlibrary['multiply']=multiply
funlibrary['invertIm']=invertIm
funlibrary['blur']=blur
funlibrary['toIm']=toIm
funlibrary['linspace']=linspace
funlibrary['sin']=sin
funlibrary['cos']=cos
funlibrary['plot']=plot




#function list
def interpreter(commands,username,cache):
    stack=[]
    for command in commands:
        #separate command
        if command.endswith("::fun"):
            fun =command[0:-5]
            #store variable
            if fun.startswith("<-"):
                name=command[2:-5]
                cache.addItem(username,name,stack.pop())
            elif not funlibary.get(fun) is None:
                funlibary.get(fun)(stack,username,cache)
        elif command.endswith("::str"):
            if command.startswith("$"):
                command=command[1:-5]
                command=cache.getItem(username,command)
                if not (command is None):
                    stack.append(command)
            else:
                command=command[:-5]
                stack.append(command)
        elif command.endswith("::number"):
            try:
                stack.append(float(command[:-8]))
            except:
                raise Exception("Type Conversion error")
    return stack

if __name__=="__main__":
    data={}
    data["commands"]=[("add",),("substract",),("unknown",)]
    data["stack"]=[2,1,0]
    result=interpreter(data)
    print(result)