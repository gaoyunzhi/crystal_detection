import os
from video_analysis import *
from slug import *


def v2img(videofilename, outputdir):
    datafilename=os.path.join(outputdir,'data.txt')
    locationfilename=os.path.join(outputdir,'location.txt')
    resultfilename=os.path.join(outputdir,'result.txt')
    #video_analysis(videofilename,datafilename)
    #find_slug(datafilename,locationfilename,resultfilename)
    position_all=[(-2,0,0)]
    f=open(locationfilename,'r')
    for line in f:
        position_all.append(map(int,line.split()))
    f.close()
    N=107 # for test
    vidcap=cv2.VideoCapture(videofilename) #for test
    #print N
    l=len(position_all)
    i=1
    slug_count=0
    while i<l-1:
        if position_all[i][2]>position_all[i+1][2]: #new slug
            length=0
            if position_all[i][0]<0:
                i+=1;continue
            while position_all[i][0]==1:
                i+=1
                if position_all[i][1]>length: length=position_all[i][1]
            if position_all[i][1]>length: length=position_all[i][1]
            if length>2: 
                if position_all[i][0]==0: 
                    shot=i
                else:
                    next_center=position_all[i][2]-position_all[i][1]/2+length/2
                    previous_center=position_all[i-1][2]-length/2+position_all[i-1][1]/2
                    shot=(i*(previous_center-N/2)+
                        (i-1)*(N/2-next_center)*1.0)/(previous_center-next_center)
                shot*=SPEED
                vidcap.set(cv.CV_CAP_PROP_POS_MSEC, shot) 
                success,image=vidcap.read()
                slug_count+=1
                cv2.imwrite(os.path.join(outputdir,'slug%d.jpg'%slug_count), image)
                print slug_count,i
            while position_all[i][0]==0 or position_all[i][0]==-1:
                i+=1
        else:
            i+=1

v2img('C:\\Dropbox\\video analysis\\062613-1.mp4','C:\\Dropbox\\video analysis\\slugs')