# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:29:38 2016

@author: wakanawakana
"""

import cv2
import numpy as np
import sys

def flo_image(flofile):
    flo = open(flofile, 'rb')

    sig = flo.read(4)
    if sig != 'PIEH':
        print 'Not flo file.'
        exit

    size = np.fromfile(flo, dtype=int, count=2)
    uv = np.fromfile(flo, dtype=np.float32, count=size[0]*size[1]*2)
    uv2 = uv.reshape(-1, 2)
    print 'umax=%f umin=%f' % (np.max(uv2[:,0]) , np.min(uv2[:,0]) )
    print 'vmax=%f vmin=%f' % (np.max(uv2[:,1]) , np.min(uv2[:,1]) )
    print 'if uv value has over range 127~-128 failed'
    yuv = np.zeros(size[0]*size[1]*3, dtype=np.uint8).reshape(-1, 3)
    yuv[:, 0] = 255
    yuv[:, 1] = uv2[:,0] + 128
    yuv[:, 2] = uv2[:,1] + 128
    yuv = yuv.reshape(size[1], size[0], 3)
    u8 = np.zeros(size[0]*size[1], dtype=np.uint8)
    u8 = uv2[:,0] + 128
    u8 = u8.reshape(size[1], size[0], 1)
    v8 = np.zeros(size[0]*size[1], dtype=np.uint8)
    v8 = uv2[:,1] + 128
    v8 = v8.reshape(size[1], size[0], 1)

    #img = np.zeros((size[0], size[1], 3), np.uint8)
    img = cv2.cvtColor(yuv, cv2.COLOR_YCrCb2RGB )
    cv2.imwrite('out_color.png', img)
    cv2.imwrite('out_u.png', u8)
    cv2.imwrite('out_v.png', v8)

if __name__ == '__main__':
    flo_image(sys.argv[1])
