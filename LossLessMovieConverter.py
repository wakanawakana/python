# -*- coding: utf-8 -*-
"""
Created on Mon May 01 11:01:01 2017
UTVideo http://umezawa.dyndns.info/wordpress/
MagicYUV https://www.magicyuv.com/
fourcc 
ULRA: UTVideo RGBA32
ULRG: UTVideo RGB24
ULY4: UTVideo YUV4:4:4 BT.601
ULY2: UTVideo YUV4:2:2 BT.601
ULH2: UTVideo YUV4:2:2 BT.709
M8RA: MagicYUV RGBA32
M8RG: MagicYUV RGB24
M8Y4: MagicYUV YUV4:4:4
M0RG: MagicYUV 10-bit RGB
M0RA: MagicYUV 10-bit RGBA
M2RG: MagicYUV 12-bit RGB
M2RA: MagicYUV 12-bit RGBA
M4RG: MagicYUV 14-bit RGB
M4RA: MagicYUV 14-bit RGBA
RGB : Uncompressed
RAW : Uncompressed
HFYU: Huffman Lossless Codec
"""

import os
import cv2
from cvVideoAccess import cvVideoAccess

if __name__ == '__main__':
    inputFile = os.path.abspath('./Video.mp4')
    outpuFile = "./out.avi"

    cvva = cvVideoAccess()
    cvva.open(inputFile)

    vwriter = cvVideoAccess()
    fourcc = cv2.VideoWriter_fourcc(*'HFYU')
    vwriter.create(outpuFile, cvva.video_width(), cvva.video_height(), cvva.video_fps(), fourcc)
    ret = True
    frameno = 1
    step = 1
    startFrame = 260
    stopFrame = 1000

#    cvva.seek_frame(startFrame)
    frameno = startFrame
    while(ret == True and stopFrame >= frameno):
        ret, frame = cvva.get_frame(frameno)
        vwriter.set_next(frame)
        frameno += step
    
