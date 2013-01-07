'''
load image file, data save in directory images
'''
import os
import cv2
from cv2 import cv
import math
import Image
import numpy
from math import sqrt
from remove_bk import rm_bk
# from PIL import Image
# import pylab
dir = 'images'
for file in os.listdir(dir):
    name, ext = os.path.splitext(file)
    if not name.isdigit(): continue
    if name!='1': continue # for test
    filename = os.path.join(dir, file)
    image_o=cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY)
    h,w=image_o.shape[:2]
    print h,w
    #image=cv.CreateMat(h / 10, w / 10, cv.CV_8UC3)
    image=cv2.resize(image_o,(w/10,h/10))
    mu, sigma = map(int,cv2.meanStdDev(image))    
    th_h=(mu+image.max())/2
    def f(x):
        if x<0: return -x/10
        if x<10: return x/10
        return 2*x/10-1
    h,w=image.shape
    for i in xrange(h):
        for j in xrange(w):
            offset=f(sqrt((i-h/2)**2+(j-w/2)**2)/6-30)
            if image[i][j]+offset>mu: image[i][j]+=offset
            if image[i][j]>th_h: image[i][j]=th_h
    path=os.path.splitext(filename)[0] + '_light.png'
    cv2.imwrite(path, image)
    new=rm_bk(image)
    path=os.path.splitext(filename)[0] + '_no_bk.png'
    cv2.imwrite(path, new)
    continue
    

    
    
    i=11
    image = cv2.bilateralFilter(orig_image,i, i*2,i/2)
    h,w=image.shape
    


    def f(x):
        if x<0: return -x
        return 3*x
    for i in xrange(h):
        for j in xrange(w):
            image[i][j]+=f(sqrt((i-h/2)**2+(j-w/2)**2)/6-50)
            if image[i][j]>th_h: image[i][j]=th_h
    clear_path=os.path.splitext(filename)[0] + '_light.png'
    cv2.imwrite(clear_path, image)
    
    mu, sigma = map(int,cv2.meanStdDev(image))    
    im_min=256
    im_max=0
    for r in image:
        for x in r:
            if x<im_min: im_min=x
            if x>im_max: im_max=x
    print mu,sigma
    print im_min,im_max
    
    th_r=(mu+im_min)/2
    th_h=(mu+im_max)/2
    print th_r
    for i in xrange(h):
        for j in xrange(w):
            if image[i][j]<th_r: 
                image[i][j]=0
            if image[i][j]>mu:
                image[i][j]=255
    clear_path=os.path.splitext(filename)[0] + '_clear.png'
    cv2.imwrite(clear_path, image)
    
    continue
    cv2.GaussianBlur(orig_image,(5,5),0)
    image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY)
    mu, sigma = cv2.meanStdDev(image)
    print int(mu+3*sigma)
    im_bw = cv2.threshold(image,int(mu-1.4*sigma), 255, cv2.THRESH_BINARY )[1]
    im_bw=cv2.bitwise_not(im_bw)
    bw_path=os.path.splitext(filename)[0] + '_bw.png'
    cv2.imwrite(bw_path, im_bw)
    
    
    
    
    
    continue
    mu, sigma = cv2.meanStdDev(image)
    edges = cv2.Canny(image, sigma, mu + sigma)
    ret_path = os.path.splitext(filename)[0] + '_edge.png'
    print ret_path
    cv2.imwrite(ret_path, edges)
    
    lines = cv2.HoughLinesP(cv2.GaussianBlur(edges,(5,5),0), 1, math.pi / 180, 20, numpy.array([]), 10,10)
    ret_path = os.path.splitext(filename)[0] + '_line.png'
    image_line=cv2.imread(filename)
    print len(lines[0])
    for l in lines[0]:
        cv2.line(image_line, (l[0],l[1]), (l[2],l[3]), (0,0,255), 3)
    print ret_path
    cv2.imwrite(ret_path, image_line)
    
