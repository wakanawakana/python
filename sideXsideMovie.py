# -*- coding: utf-8 -*-


import os
import numpy as np
from cvVideoAccess import cvVideoAccess


def sideflame(left, right, h, w):
    marge = np.zeros((h, w, 3), dtype=np.uint8)
    lw = left.shape[1]
    rw = right.shape[1]
    marge[:,0:lw,:] = left[:,:,:]
    marge[:,lw:lw+rw,:] = right[:,:,:]
    return marge
    
if __name__ == '__main__':
    inputFile1 = os.path.abspath('./1.mp4')
    inputFile2 = os.path.abspath('./2.mp4')
    outpuFile = "test_side.mp4"
    
    cvva1 = cvVideoAccess()
    cvva1.open(inputFile1)

    cvva2 = cvVideoAccess()
    cvva2.open(inputFile2)

    vwriter = cvVideoAccess()
    h = int(max(cvva1.height, cvva2.height))
    w = int((cvva1.width + cvva2.width))
    vwriter.set_forcc('H264')
    vwriter.create(outpuFile, w, h, 30)
    
    for frameno in range(0, 0+300):
        ret, right = cvva1.get_frame(frameno)
        ret, left = cvva2.get_frame(frameno)
        marge = sideflame(left, right, h, w)
        vwriter.set_next(marge)

    vwriter.close()

