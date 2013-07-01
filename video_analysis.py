#!/usr/bin/env python
from cv2 import cv
import cv2

N=100
M=10
SPEED=300

def avglight(image):   
    avgl=[]
    for i in xrange(w/(2*N),w,w/N):
        s=0
        for j in xrange(h/(2*M),h,h/M):
            s+=sum(image[j][i])
        avgl.append(s)
    return avgl

def test_range(x):
    if x in [1344]: return True
    return False

def video_analysis(filename,datafilename):
    global h,w,vidcap
    vidcap=cv2.VideoCapture(filename)
    success,image=vidcap.read()
    h,w=image.shape[0],image.shape[1]
    count=1
    compare_all=[]    
    f=open(datafilename,'w')
    f.close()
    while True:
        if not test_range(count): 
            count+=1
            continue
        vidcap.set(cv.CV_CAP_PROP_POS_MSEC, count*SPEED) 
        success,image=vidcap.read()
        if not success: break
        if test_range(count):
            cv2.imwrite('pic\\frame%d.jpg'%count, image)
        avgl=avglight(image)        
        count+=1
        f=open(datafilename,'a')
        f.write('\t'.join(map(str,avgl))+'\n')
        f.close()
    
                
#video_analysis('C:\\TDDOWNLOAD\\062613-1.mp4','tmp.txt')