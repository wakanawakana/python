# -*- coding: utf-8 -*-
"""
Image inflater 
Created on Tue Feb 21 13:44:58 2017
"""

import os
import re
import sys
import cv2
import glob
from scipy import ndimage

if __name__ == '__main__':
    mode = 2
    filelist = glob.glob("./Images/I_tool/*.png")
    for n in range(0, len(filelist)):
        savefile = filelist[n].replace("I_tool", "I_tool_inv")
        if mode == 0:
            img = cv2.imread(filelist[n], cv2.IMREAD_GRAYSCALE)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif mode == 1:
            img = cv2.imread(filelist[n])
            img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            img_h, img_s, img_v = cv2.split(img)
            img = cv2.cvtColor(img_v, cv2.COLOR_GRAY2RGB)
        elif mode == 2:
            img = cv2.imread(filelist[n])
            img = cv2.bitwise_not(img)
        elif mode == 3: #90
            img = cv2.imread(filelist[n])
            img = ndimage.rotate(img, 90, reshape=True)
        elif mode == 4: #180
            img = cv2.imread(filelist[n])
            img = cv2.flip(img, -1)
        elif mode == 5: #270
            img = cv2.imread(filelist[n])
            img = ndimage.rotate(img, 270, reshape=True)
        elif mode == 6: #resize 1/2
            img = cv2.imread(filelist[n])
            feald_image = np.zeros((img.shape[0]/2, img.shape[1]/2, 3), dtype=np.uint8)
            for n in range(0, img.shape[0]/2-1):
                for i in range(0, img.shape[1]/2-1):
                    feald_image[n,i,:] = img[n*2 + 0,i*2,:]
            img = feald_image
        elif mode == 7: #LBP
            img = cv2.imread(filelist[n], cv2.IMREAD_GRAYSCALE)
            img = local_binary_pattern(img, 8, 1)            

        cv2.imwrite(savefile, img)
            
        
        
        
