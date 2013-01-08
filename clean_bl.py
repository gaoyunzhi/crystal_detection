'''
clean blocks
'''
from math import sqrt
import cv2
from cv2 import cv
from numpy import *
from random import randint

def overlap(u,v):
    n1,x1,y1,lst1=u
    n2,x2,y2,lst2=v    
    dis=sqrt((x1-x2)**2+(y1-y2)**2)
    if dis<max(sqrt(n1),sqrt(n2))-1:
        return True
    return False
    
def clean_bl(blocks,image,img_color):
    N=image.size
    info=[]
    for i in xrange(len(blocks)):
        avg,elts=blocks[i]
        x=0;y=0;n=0
        for e in elts:
            x+=e[0]
            y+=e[1]
            n+=1
        if n>N/5: 
            for u,v in elts:
                img_color[u][v]=array([255,255,255])
            continue
        info.append([n,x*1.0/n,y*1.0/n,[i]])
    info.sort()
    info.reverse()
    m=len(info)
    for l in xrange(m):
        if info[l][0]==1: break
    for i in xrange(m):
        for j in xrange(min(i,l)):
            if info[j]==None: continue
            if overlap(info[i],info[j]):
                n1,x1,y1,lst1=info[i]
                n2,x2,y2,lst2=info[j]
                info[i]=[n1+n2,(x1*n1+x2*n2)/(n1+n2),(y1*n1+y2*n2)/(n1+n2),lst1+lst2]
                info[j]=None
                break
    info=[x for x in info if x!=None and x[0]>4]
    combined=[]
    for n,x,y,lst in info:
        current=[]
        color=[randint(0,255),randint(0,255),randint(0,255)]
        for i in lst:
            for u,v in blocks[i][1]:
                img_color[u][v]=array(color)
                current.append((u,v))
        combined.append(current)
    
                
    print len(info)
    return img_color,combined
            

                
        
        