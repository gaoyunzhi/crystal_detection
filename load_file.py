'''
load image file, data save in directory images
'''
import os
import cv2
# from PIL import Image
# import pylab
dir = 'images'
for file in os.listdir(dir):
    name, ext = os.path.splitext(file)
    if not name.isdigit(): continue
    filename = os.path.join(dir, file)
    image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY)
    im_bw = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    bw_path=os.path.splitext(filename)[0] + '_bw.png'
    cv2.imwrite(bw_path, im_bw)
    mu, sigma = cv2.meanStdDev(im_bw)
    edges = cv2.Canny(image, mu - sigma, mu + sigma)
    ret_path = os.path.splitext(filename)[0] + '_bw_edge.png'
    print ret_path
    cv2.imwrite(ret_path, edges)
