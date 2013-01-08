'''
load image file, data save in directory images
'''
import os
import cv2
from resize import resize
from flood import flood
from clean_bl import clean_bl
from cal_shape import cal_shape
dir = 'images'
for file in os.listdir(dir):
    name, ext = os.path.splitext(file)
    if not name.isdigit(): continue
    if name!='1': continue # for test
    filename = os.path.join(dir, file)
    orig=cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY)
    image=resize(orig)
    color=resize(cv2.imread(filename))
    
    
    flooded,blocks,bk=flood(image)
    path=os.path.splitext(filename)[0] + '_flooded.png'
    cv2.imwrite(path, flooded)
    combined_img,combined=clean_bl(blocks,image,color)
    path=os.path.splitext(filename)[0] + '_blocks.png'
    cv2.imwrite(path, combined_img)
    
    for x in combined:
        cal_shape(x)
    
    

    
