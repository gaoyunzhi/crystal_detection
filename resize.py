'''
resize image
'''
from math import sqrt
import cv2
N=10000

def resize(image):
    h,w=image.shape[:2]
    if len(image.shape)==3:
        r=3
    else:
        r=1
    scale=int(sqrt(image.size/N/r))
    return cv2.resize(image,(w/scale,h/scale))
