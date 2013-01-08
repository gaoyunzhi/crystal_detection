'''
calculate shape constants
'''
import cv2
import numpy
from numpy import *

def cal_shape(pts):
    ret=cv2.convexHull(numpy.array([[[x,y]] for x,y in pts]))
    (x,y),(w,h),t = cv2.minAreaRect(ret)
    print x,y,w,h, cv2.contourArea(ret)
    