# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 15:49:07 2017
Movie to PNG Converter
"""

import os
import cv2
from cvVideoAccess import cvVideoAccess

if __name__ == '__main__':
    inputFile = os.path.abspath('./Video.mp4')
    outdir = os.path.abspath('C:\\Users\\wakanawakana\\mLearn\\movie\\images')
    output_form = 'case1_frame_{:06d}.png'
    
    cvva = cvVideoAccess()

    cvva.open(inputFile)
    ret = True
    frameno = 1
    step = 1
    startFrame = 3270
    stopFrame = startFrame + 120

    frameno = startFrame
    while(ret == True and stopFrame > frameno):
        outputName = output_form.format(frameno)
        outfpath = os.path.join(outdir, outputName)

        ret, frame = cvva.get_frame(frameno)
        cv2.imwrite(outfpath, frame)
        frameno += step
