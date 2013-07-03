import os,cv2
from cv2 import cv
#from video_analysis import *
#from slug import *

w=744
h=480
V_INTVAL=5 #better to be odd number
H_N=100
H_INTVAL=w/H_N
MARGIN_WIDTH_PRECENTAGE_L=0.03
N=len(xrange(H_INTVAL/2,w,H_INTVAL))
MARGIN_WIDTH_L=int(N*MARGIN_WIDTH_PRECENTAGE_L)
MARGIN_WIDTH_PRECENTAGE_H=0.2
MARGIN_WIDTH_H=int(N*MARGIN_WIDTH_PRECENTAGE_H)
TH_L=20
GRAD_TH=50
    

def test_range(x):
    return False

def to_str(x): # for test
    if x<10:return '|'
    if x<20: return str(int(x-10))
    if x<30:return '+'
    if x>100: return 'o'
    return '-'

def lightness(image,hight):
    SAMPLE_N=10;SAMPLE_DIS=w/SAMPLE_N
    samples=[sum(image[hight][x]) for x in xrange(SAMPLE_DIS/2,w,SAMPLE_DIS)]
    samples.sort()
    return samples[SAMPLE_N/2]
        
def update_horizontal_center(image):
    global horizontal_center
    grad=8 
    while grad!=1:
        current_light=lightness(image,horizontal_center)
        higher_center=max(horizontal_center-grad,0)
        lower_center=min(horizontal_center+grad,h-1)
        higher_light=lightness(image,higher_center)
        lower_light=lightness(image,lower_center)
        max_light=max(current_light,higher_light,lower_light) 
        #if grad<3 and max_light-min(current_light,higher_light,lower_light)>GRAD_TH or max_light<GRAD_TH:
        #    grad=50
        #    continue
        if current_light==max_light:
            grad/=2
            continue
        if higher_light==max_light:
            horizontal_center=higher_center
        else:
            horizontal_center=lower_center
        grad=min(20,int(1.5*grad))
        
 
def find_slug(msec):
    vidcap.set(cv.CV_CAP_PROP_POS_MSEC, msec) 
    success,image=vidcap.read()
    if not success: return 'video end' # end of the video
    update_horizontal_center(image)
    lightness=[]
    for x in xrange(H_INTVAL/2,w,H_INTVAL):
        s=0
        for y in xrange(horizontal_center-V_INTVAL,horizontal_center+V_INTVAL+1,2):
            s+=sum(image[y][x])*1.0/len(image[y][x])
        lightness.append(s/(V_INTVAL+1))
    #print ''.join(map(to_str,lightness))
    has_leftmargin=False
    has_rightmargin=False
    for leftmargin in xrange(N-MARGIN_WIDTH_L):
        if lightness[leftmargin]<TH_L and \
            sum(lightness[leftmargin:leftmargin+MARGIN_WIDTH_L])<MARGIN_WIDTH_L*TH_L:
            has_leftmargin=True
            break
    for rightmargin in xrange(N-1,MARGIN_WIDTH_L-2,-1):
        if lightness[rightmargin]<TH_L and \
            sum(lightness[rightmargin-MARGIN_WIDTH_L+1:rightmargin+1])<MARGIN_WIDTH_L*TH_L:
            has_rightmargin=True
            break
    assert (has_leftmargin==has_rightmargin) or (leftmargin<MARGIN_WIDTH_L*2) or (rightmargin>=N-MARGIN_WIDTH_L*2-1)
    if has_leftmargin==has_rightmargin==False: return
    has_leftinner=False
    for leftinner in xrange(leftmargin+1,min(N,leftmargin+MARGIN_WIDTH_H)):
        if lightness[leftinner]>TH_L and \
            sum(lightness[leftinner:min(leftinner+MARGIN_WIDTH_L,N)])>(min(leftinner+MARGIN_WIDTH_L,N)-leftinner)*TH_L: 
            has_leftinner=True
            break
    if not has_leftinner:
        if not leftinner==N-1: return
        leftinner=N
    has_rightinner=False
    for rightinner in xrange(rightmargin-1,max(-1,rightmargin-MARGIN_WIDTH_H),-1):
        if lightness[rightinner]>TH_L and \
            sum(lightness[max(rightinner-MARGIN_WIDTH_L+1,0):rightinner+1])>(rightinner+1-max(rightinner-MARGIN_WIDTH_L+1,0))*TH_L: 
            has_rightinner=True
            break
    if not has_rightinner:
        if not rightinner==0: return
        rightinner=-1
    if abs(rightinner-leftmargin)<=MARGIN_WIDTH_L or rightmargin-leftmargin<MARGIN_WIDTH_L*3\
        or abs(rightmargin-leftinner)<=MARGIN_WIDTH_L:
        ret= (leftmargin+rightinner)/2.0, (leftinner+rightmargin)/2.0
    else:
        ret= leftmargin,leftinner,rightinner,rightmargin
    return ret
    
def scale(x):
    return x*100.0/N
def float_to_str(x):
    return "%.2f" %x

def v2img(videofilename, outputdir):
    global horizontal_center,vidcap,t3
    resultfilename=os.path.join(outputdir,'slug.txt')
    vidcap=cv2.VideoCapture(videofilename)
    SPEED=290.0 
    msec=0.0
    horizontal_center=h/2
    slugs=[]
    slug_number=0
    while True:
        msec+=SPEED
        ret=find_slug(msec)
        if ret=='video end': break        
        if not ret:    
            continue
        if len(ret)==2:
            m1=msec
            sp=SPEED/2
            m2=m1+sp
            r1=ret[:]
            r2=find_slug(m2)
            if r2=='video end': break # not likely to happen
            try:
                assert r2
            except:
                continue
            if len(r2)==2:
                try:
                    sp*=max(N/2.0/max((r1[0]-r2[0]),(r1[1]-r2[1])),1.8)
                except:
                    print m1,m2,r1,r2
                m2=m1+sp
                r2=find_slug(m2)
                if r2=='video end': break # not likely to happen                
        else:
            m2=msec
            r2=ret[:]
            sp=SPEED/4
            m1=msec-sp
            r1=find_slug(m1)
            if r1=='video end': break # not likely to happen
            assert r1
        try:
            length=r2[3]-r2[0]+1
        except:
            continue
        inner_length=r2[2]-r2[1]+1
        desire_left_end=(N-1-length)*0.5
        m=(m1*(r2[0]-desire_left_end)+m2*(desire_left_end-r1[0]))/(r2[0]-r1[0])
        fs=find_slug(m)
        if len(fs)!=4: continue
        slug_number+=1
        vidcap.set(cv.CV_CAP_PROP_POS_MSEC, m) 
        success,image=vidcap.read()
        cv2.imwrite(os.path.join(outputdir,'slug%d.jpg'%slug_number), image)
        SPEED=N*0.67*sp/(r1[0]-r2[0])
        desire_left_end=-length*1.2+MARGIN_WIDTH_H
        msec=(m1*(r2[0]-desire_left_end)+m2*(desire_left_end-r1[0]))/(r2[0]-r1[0])        
        length=length*100.0/N
        inner_length=inner_length*100.0/N
        fs=map(scale,fs)
        slugs.append([slug_number,m,length,inner_length,(r1[0]-r2[0])/(m2-m1)*100000.0/N,horizontal_center]+fs)
    with open(resultfilename,'w') as f:
        for line in slugs:
            f.write('\t'.join(map(float_to_str,line))+'\n')    
        m=len(slugs)
        avglen=sum([x[2] for x in slugs])/m
        avgcenterlen= sum([x[3] for x in slugs])/m
        f.write('avg length '+float_to_str(avglen)+'\n')
        f.write('avg center length '+float_to_str(avgcenterlen)+'\n')


#v2img('C:\\Dropbox\\video analysis\\062613\\062613-1.mp4','C:\\Dropbox\\video analysis\\slugs')
