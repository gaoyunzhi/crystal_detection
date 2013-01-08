'''
fill in colors by parts, grey scale image
'''
from itertools import product
import numpy
from cv2 import cv
import cv2

Th=30
neighbor=list(product(xrange(-1,2),xrange(-1,2)))
neighbor.remove((0,0))

def flood(image):    
    h,w=image.shape
    flooded= image.copy()
    visited=set()
    bk=255
    blocks=[]
    for c_x,c_y in product(xrange(h),xrange(w)):
        if (c_x,c_y) in visited: continue
        aganda=[(c_x,c_y)]
        visited.add((c_x,c_y))
        sum=int(image[c_x][c_y])
        num=1
        p=0
        while p<len(aganda):
            u,v=aganda[p]
            p+=1
            flag=0
            for i,j in neighbor:
                x,y=u+i,v+j
                if not (0<=x<h and 0<=y<w): continue
                if abs(int(image[x][y])-image[u][v])<Th:
                    flag+=1
            if flag<=6: continue
            for i,j in neighbor:
                x,y=u+i,v+j
                if not (0<=x<h and 0<=y<w): continue
                if abs(int(image[x][y])-image[u][v])<Th and not (x,y) in visited:
                    aganda.append((x,y))  
                    visited.add((x,y))
                    sum+=image[x][y]
                    num+=1              
        avg=sum/num
        if len(aganda)>h*w/5: 
            bk=avg
        blocks.append([avg,aganda])
    for avg, aganda in blocks:
        for x,y in aganda:
            flooded[x][y]=avg
    return flooded,blocks,bk
        
            
            
    