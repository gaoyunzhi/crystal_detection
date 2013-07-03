import os,cv2,random
from cv2 import cv
import numpy as np
from v2img import V_INTVAL,TH_L
from flood import flood
import random,math
N=7
w=744
h=480
TH_W=50


def scale(x):
    return int(x*w/100.0)

def float_to_str(x):
    return "%.2f" %x

def find_margin(image,left,right):   
    for l in xrange(left-3,left+4):
        s=0.0
        for y in xrange(horizontal_center-V_INTVAL,horizontal_center+V_INTVAL+1,2):
                s+=image.item(y,l)
        if s/(V_INTVAL+1)>TH_L: break
    for r in xrange(right+3,right-4,-1):
        s=0.0
        for y in xrange(horizontal_center-V_INTVAL,horizontal_center+V_INTVAL+1,2):
                s+=image.item(y,l)
        if s/(V_INTVAL+1)>TH_L: break
    return l,r
        
        
def crystal_detection(dir,filename,videofilename):
    global horizontal_center
    vidcap=cv2.VideoCapture(videofilename)
    slug_number=int(filename[4:-4])
    msec,length,innerLength,speed,horizontal_center=info[slug_number][:-4]
    horizontal_center=int(horizontal_center)
    leftmargin,leftinner,rightinner,rightmargin=map(scale,info[slug_number][-4:])
    mm=3000.0/speed
    im=[]
    for i in xrange(2*N+1):
        m=msec+(i-N)*mm
        vidcap.set(cv.CV_CAP_PROP_POS_MSEC, m) 
        success,image=vidcap.read()
        if i==N:
            im_o=image[:,:]
            im_o_bw=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        im.append(cv2.cvtColor(image,cv2.COLOR_RGB2GRAY))
        cv2.imwrite(os.path.join(dir,'crystal_%d_raw_%d.jpg'%(slug_number,i)), im[i])
    tmp=im[N][:,:]
    left,right=find_margin(im[N],leftinner,rightinner)
    for i in xrange(h):
        for j in xrange(left,right+1):
            colors=[im[x].item(i,j) for x in xrange(2*N+1) if x!=N]
            if sum([abs(x-im[N].item(i,j))<=5 for x in colors])>N*0.6:
                tmp.itemset(i,j,255)
                continue
            colors=[]
            for x in xrange(2*N+1):
                if x==N: continue
                j1=j-(x-N)*0.03*w
                if 0>j1 or j1>=w: continue
                colors.append(im[x].item(i,j1))
            if sum([abs(x-im[N].item(i,j))<=5 for x in colors])>len(colors)*0.3:
                tmp.itemset(i,j,255)
                continue
            tmp.itemset(i,j,0)
    tmp=tmp[:,left:right+1]
    width=right+1-left
    blocks=flood(tmp,h,width)
    cv2.imwrite(os.path.join(dir,'crystal_%d_middle.jpg'%slug_number), tmp)
    for area,min_rec,components,convexhull in blocks:
        c=0.0;b=[255.0]
        components=set(components)
        for i,j in components:
            c+=im_o_bw.item(i,j+left)
            for x in xrange(5):
                u=i+random.randint(-5,5)
                v=j+random.randint(-5,5)
                if (u,v) in components: 
                    continue
                if not ((0<=u<h) and (0<=v<w)): continue
                b.append(im_o_bw.item(u,v))
        b.sort()
        b=b[len(b)/2]    
        c/=len(components)
        if c>b+20: continue
        color=[random.randint(150,256) for x in xrange(3)]
        [[u1,v1]]=convexhull[-1]
        for [[u2,v2]] in convexhull:
            le=int(math.sqrt((u1-u2)**2+(v1-v2)**2)*1.2)+2
            for ratio in xrange(le):
                r=ratio*1.0/(le-1)
                i=int(u1*r+(1-r)*u2+0.0001)
                j=int(v1*r+(1-r)*v2+0.0001)
                for x in xrange(3):
                    im_o.itemset(i,j+left,x,color[x])
            u1,v1=u2,v2
        (u1,v1),(u2,v2),t=min_rec
        with open(os.path.join(dir,'result.txt'),'a') as f:
            f.write('\t'.join([str(slug_number)]+
                              map(float_to_str,(u1,v1+left,u2,v2)))+'\n')
        #print '\t'.join([str(slug_number)]+map(float_to_str,(u1,v1+left,u2,v2))),c,b
    cv2.imwrite(os.path.join(dir,'crystal_%d_final.jpg'%slug_number), im_o)
    cv2.imwrite(os.path.join(dir,'final_%d.jpg'%slug_number), im_o)
    print slug_number

        
dir='C:\\Dropbox\\video analysis\\slugs'
info=[()]
with open(os.path.join(dir,'slug.txt'),'r') as f:
    for line in f:
        try:
            info.append(map(float,line.split())[1:])
        except:
            break
for file in ['slug133.jpg']+os.listdir(dir):
    if file.startswith('slug') and file.endswith('.jpg'):
        crystal_detection(dir,file,'C:\\Dropbox\\video analysis\\062513\\062613-1.mp4')