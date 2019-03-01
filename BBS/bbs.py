# -*- coding: utf-8 -*-
"""
Created on Fri Mar 01 13:08:56 2019
@author: wakanawakana
Best-Buddies Similarity for Robust Template Matching (CVPR2015)
https://arxiv.org/pdf/1609.01571.pdf
"""

import cv2
import numpy as np
import numpy.matlib as matlib

class BestBuddiesSimilarity:
    def __init__(self):
        return
        
    def __del__(self):
        return
    
    def im2col(self, A, B, mode='sliding'):
        # Parameters
        if A.ndim == 2: # grayscale
            M,N = A.shape
            D = 1
        else:    
            M,N,D = A.shape
        col_extent = N - B[1] + 1
        row_extent = M - B[0] + 1
        # Get Starting block indices
        start_idx = np.arange(B[0]).T[:,None] + np.arange(B[1])*N
        # Generate Depth indeces
        didx=N*np.arange(1)
        start_idx=(didx[:,None]+start_idx.ravel()).reshape((-1,B[0],B[1]))
        # Get offsetted indices across the height and width of input array
        offset_idx = np.arange(col_extent).T[:,None] + np.arange(row_extent)*N
        # Get all actual indices & index into input array for final output
        if mode == 'distinct':
            take_ind = start_idx.ravel()[:,None] + offset_idx[::B[0],::B[1]].ravel()
        else:
            take_ind = start_idx.ravel()[:,None] + offset_idx.ravel()

        out = np.empty([B[0]*B[1], take_ind.shape[1],D])
        for i in range(D):
            out[:,:,i] = np.take(A, take_ind*D+i)
        return out

    def gausian(self, shape, sigma, N):
        m,n = [(ss-1.)/2. for ss in shape]
        y,x = np.ogrid[-m:m+1,-n:n+1]
        coef = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
        coef[ coef < np.finfo(coef.dtype).eps*coef.max() ] = 0
        sumc = coef.sum()
        if sumc != 0:
            coef /= sumc
        fmat = coef.reshape(coef.size, 1)
        return fmat
   
    def distance(self, temp_shape, pz):
        ny, nx = temp_shape
        dxy = np.zeros([(ny/pz)*(nx/pz), (ny/pz)*(nx/pz)])
        xx, yy = np.meshgrid( np.arange(0,nx-1,pz)*0.0039, np.arange(0,ny-1,pz)*0.0039)
        xx_ = xx.ravel()
        yy_ = yy.ravel()
        for i in range(xx.size):
            dxy[i,:] = (xx_ - xx_[i])**2 + ((yy_ - yy_[i])**2)
        return dxy
    
    def BBS_calc(self, Imat, Tmat, Indmat, drgb, dxy, drgbbuf, bbp1, bbp2, bbs, nrage, gamma, N, xn, yn, twpz, thpz):
        for x in range(0, xn):
            for y in range(0, yn):
                if (y==0 and x==0): # compute full distance matrix for first image patch
                    ind = Indmat[0:thpz, 0:twpz]
                    crop = Imat[:,ind.T.ravel()]
                    for p in range(N):
                        tmp = (crop[:,p][:,np.newaxis] - Tmat)**2
                        drgb[:,p] = np.sum(np.sum(tmp, axis=2), axis=0)
                elif (y>0 and x==0):
                    # use data computed for previous candidates
                    # Push the computed values one row up (pixel (2,1)-->(1,1))
                    drgb = np.roll(drgb, -1, axis=1)
                    ind = Indmat[y:y+thpz, 0:twpz]
                    crop = Imat[:,ind.T.ravel()]
                    indxp = thpz-1
                    for p in range(twpz):
                        tmp = (crop[:,p][:,np.newaxis] - Tmat)**2
                        drgb[:,indxp] = np.sum(np.sum(tmp, axis=2), axis=0)
                        indxp += thpz
                elif (y==0 and x>0):
                    drgb_ = drgbbuf[:,:,0]
                    drgb[:,0:drgb.shape[1]-1-thpz] = drgb_[:,thpz+1:]
                    ind = Indmat[0:y+thpz, x+twpz]
                    crop = Imat[:,ind.T.ravel()]
                    indxp = thpz*(twpz-1)-1
                    for p in range(thpz):
                        tmp = (crop[:,p][:, np.newaxis] - Tmat)**2
                        drgb[:,indxp] = np.sum(np.sum(tmp, axis=2), axis=0)
                        indxp += 1
                else:
                    drgb = np.roll(drgb, -1, axis=1)
                    drgb_ = drgbbuf[:,:,y]
                    drgb[:,thpz-1:N-thpz:thpz] = drgb_[:,2*thpz-1::thpz]
                    ind = Indmat[y+thpz-1, x+twpz-1]
                    crop = Imat[:,ind]
                    tmp = (crop[:, np.newaxis] - Tmat)**2
                    drgb[:,-1] = np.sum(np.sum(tmp, axis=2), axis=0)
                '''
                ind = Indmat[y:y+thpz, x:x+twpz]
                crop = Imat[:,ind.T.ravel()]
                for p in range(N):
                    tmp = (crop[:,p][:,np.newaxis] - Tmat)**2
                    drgb[:,p] = np.sum(tmp, axis=0)
                '''
    
                drgbbuf[:,:,y] = drgb
                D = gamma * dxy + drgb
                idx1 = np.argmin(D, axis=0)
                idx2 = np.argmin(D, axis=1)
                bbp1.fill(0)
                bbp2.fill(2)
                bbp1[idx1,nrage]= 1
                bbp2[nrage,idx2]= 1
                bbs[y,x]=np.sum(bbp1 == bbp2)
 

    def BBS(self, Template, Image, pz, gamma):
        th, tw = Template.shape[0:2]
        xn = Image.shape[1]/pz - tw/pz
        yn = Image.shape[0]/pz - th/pz
        bbs = np.zeros([yn, xn], dtype=np.int32)

        Tmat = self.im2col(Template, [int(pz),int(pz)], 'distinct')
        Imat = self.im2col(Image, [int(pz),int(pz)], 'distinct')
        N = Tmat.shape[1]

        if Template.ndim == 2:
            Fmat = np.tile((self.gausian([pz,pz], 0.6, N))[:, np.newaxis], [1, 1])
        elif Template.shape[2] != Image.shape[2]: return None, None, None
        Fmat = np.tile((self.gausian([pz,pz], 0.6, N))[:, np.newaxis], [1, 3])

        Imat = Imat * Fmat
        Tmat = Tmat * Fmat
        dxy = self.distance(Template.shape[:2], pz)
        Indmat = np.arange(Imat.shape[1]).reshape(np.array([Image.shape[1],Image.shape[0]])/pz).T
        drgb = np.empty((N,N))
        drgbbuf = np.zeros((N, N, Image.shape[0] - Template.shape[0]))
        bbp1 = np.empty((N,N), dtype=np.uint8)
        bbp2 = np.empty((N,N), dtype=np.uint8)
        nrage = np.arange(N)
        twpz = tw/pz
        thpz = th/pz

        self.BBS_calc(Imat, Tmat, Indmat, drgb, dxy, drgbbuf, bbp1, bbp2, bbs, nrage, gamma, N, xn, yn, twpz, thpz)

        bbs = bbs.astype(np.float) / N
        bbs = cv2.resize(bbs, (xn*3, yn*3))
        max_pt = divmod(np.argmax(bbs), bbs.shape[1])
        max_pt = (max_pt[1], max_pt[0]) # opencv style
        max_value = bbs[max_pt[0], max_pt[1]]
        return max_pt, max_value, bbs
