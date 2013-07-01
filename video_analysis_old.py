#!/usr/bin/env python

from cv2 import cv
import cv2
import sys


def video_analysis(file):
    g_capture = cv.CreateFileCapture(file)
    print g_capture
    img=cv.QueryFrame(g_capture)
    print img
    cv2.imwrite('i1.png', g_capture)
    #cv2.imwrite('i1.png', g_capture)
        
    
   # print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)
   # print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)

    '''for i in xrange(10000):
        frame = cv.QueryFrame(capture)
        if frame:
            print frame'''
                
video_analysis('C:\TDDOWNLOAD\062613-1.mp4')