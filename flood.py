'''
fill in colors by parts, grey scale image
'''
from itertools import product
import numpy
from cv2 import cv
import cv2
neighbor=[(-1,0),(0,1),(1,0),(0,-1)]
TH_L_SIZE=5
TH_H_SIZE=1000
LEN_H_TH=60
LEN_L_TH=3

def flood(image,hh,ww): 
    blocks=[]
    for c_x,c_y in product(xrange(hh),xrange(ww)):
        if image.item(c_x,c_y)!=0: continue
        agenda=[(c_x,c_y)]
        image.itemset(c_x,c_y,1)
        p=0
        while p<len(agenda):
            u,v=agenda[p]
            p+=1
            for i,j in neighbor:
                x,y=u+i,v+j
                if not (0<=x<hh and 0<=y<ww): continue              
                if image.item(x,y)!=0: continue
                agenda.append((x,y))   
                image.itemset(x,y,1)
        if p<TH_L_SIZE or p>TH_H_SIZE: continue
        convexhull=cv2.convexHull(numpy.array([[[x,y]] for x,y in agenda]))
        (x,y),(w,h),t = cv2.minAreaRect(convexhull)
        area=cv2.contourArea(convexhull)
        if area<1: continue
        if max(w,h)>LEN_H_TH or min(w,h)<LEN_L_TH: continue
        blocks.append([area, ((x,y),(w,h),t ),agenda[:],convexhull])
    return blocks
        
            
            
    