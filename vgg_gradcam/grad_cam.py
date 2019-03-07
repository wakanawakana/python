#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Used with chainer-imagenet-vgg
#  https://github.com/mitmul/chainer-imagenet-vgg

import argparse
import numpy as np
import cv2
from VGGNet import VGGNet
from chainer import cuda
from chainer import serializers
import backprop
import copy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=int, default=-1)
    parser.add_argument('--image', type=str, default='images/dog.jpg')
    parser.add_argument('--label', type=int, default=207)
    parser.add_argument('--layer', type=str, default='conv2_1')
    args = parser.parse_args()

    mean = np.array([103.939, 116.779, 123.68])
    img = cv2.imread(args.image).astype(np.float32)
    fimg = cv2.resize(img, (224, 224))
#    img = cv.imread("images/dog.jpg").astype(np.float32)
    img -= mean
    img = cv2.resize(img, (224, 224)).transpose((2, 0, 1))
    img = img[np.newaxis, :, :, :]
    vgg = VGGNet()
    serializers.load_hdf5('VGG.model', vgg)

    if args.gpu >= 0:
#        cuda.get_device(args.gpu).user()
        cuda.get_device(args.gpu)
        vgg.to_gpu()
        img = cuda.cupy.asarray(img, dtype=np.float32)

    grad_cam = backprop.GradCAM(vgg)
    guided_backprop = backprop.GuidedBackprop(copy.deepcopy(vgg))
    gcam = grad_cam.generate(img, args.label, args.layer)
    gbp = guided_backprop.generate(img, args.label, args.layer)

    ggcam = gbp * gcam[:, :, np.newaxis]
    ggcam -= ggcam.min()
    ggcam = 255 * ggcam / ggcam.max()
    cv2.imwrite('ggcam.png', ggcam)

    gbp -= gbp.min()
    gbp = 255 * gbp / gbp.max()
    cv2.imwrite('gbp.png', gbp)

    heatmap = cv2.applyColorMap(gcam, cv2.COLORMAP_JET)
    gcam = fimg + np.float32(heatmap)
    gcam = 255 * gcam / gcam.max()
    cv2.imwrite('gcam.png', gcam)
