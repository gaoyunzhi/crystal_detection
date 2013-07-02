import os,cv2
from cv2 import cv

def crystal_detection(dir,filename,videofilename):
    vidcap=cv2.VideoCapture(videofilename)
    msec=100*int(filename[4:-4])
    for m in xrange(msec-300,msec+300,50):
        vidcap.set(cv.CV_CAP_PROP_POS_MSEC, m) 
        success,image=vidcap.read()
        print 'slug%.1f.jpg'%(int(m/10)/10.0)
        cv2.imwrite(os.path.join(dir,'slug%.1f.jpg'%(int(m/10)/10.0)), image)
    


dir='C:\\Dropbox\\video analysis\\slugs'
for file in os.listdir(dir):
    if file.endswith("3413.jpg"):
        crystal_detection(dir,file,'C:\\Dropbox\\video analysis\\062613-1.mp4')