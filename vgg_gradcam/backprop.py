#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

import chainer
import chainer.functions as F
from chainer import cuda
from chainer import utils

class GuidedReLU(chainer.Function):
    def __init__(self):
        self.input_data = []
        self.output_data = []
        self.chainer_version = chainer.__version__.split('.')
        return
        
    def forward_cpu(self, x):
        if int(self.chainer_version[0]) > 2:
            self.retain_inputs(())
            self.retain_outputs((0,))
            y = self.xp.maximum(x[0], 0)
        else:
            self.input_data.append(x)
            y = np.maximum(x[0], 0)        
            self.output_data.append(y)
        return y,

    def forward_gpu(self, x):
        xp = chainer.cuda.get_array_module(x[0])
        if int(self.chainer_version[0]) > 2:
            self.retain_inputs(())
            self.retain_outputs((0,))
            y = xp.maximum(x[0], 0)
        else:
            self.input_data.append(x)
            y = np.maximum(x[0], 0)        
            self.output_data.append(y)
            
        return y,

    def backward_cpu(self, x, gy):
        y = self.output_data[0]
        return utils.force_array(gy[0] * (y > 0) * (gy[0] > 0)),

    def backward_gpu(self, x, gy):
        y = self.output_data[0]
        gx = cuda.elementwise(
            'T y, T gy', 'T gx',
            'gx = (y > 0 && gy > 0) ? gy : (T)0',
            'relu_bwd')(y, gy[0])
        return gx,


class BaseBackprop(object):
    def __init__(self, model):
        self.model = model
        self.xp = model.xp
        self.chainer_version = chainer.__version__.split('.')

    def backward(self, x, label, layer):
        if int(self.chainer_version[0]) > 2:
            with chainer.using_config('train', False):
                acts = self.model.extract(x, layers=[layer, 'prob'])
        else:
            acts = self.model.extract(x, layers=[layer, 'prob'])
            

        one_hot = self.xp.zeros((1, 1000), dtype=np.float32)
        if label == -1:
            one_hot[:, acts['prob'].data.argmax()] = 1
        else:
            one_hot[:, label] = 1

        self.model.cleargrads()
        loss = F.sum(chainer.Variable(one_hot) * acts['prob'])
        loss.backward(retain_grad=True)

        return acts


class GradCAM(BaseBackprop):
    def generate(self, x, label, layer):
        acts = self.backward(x, label, layer)
        weights = self.xp.mean(acts[layer].grad, axis=(2, 3))
        gcam = self.xp.tensordot(weights[0], acts[layer].data[0], axes=(0, 0))
        gcam = (gcam > 0) * gcam / gcam.max()
        gcam = chainer.cuda.to_cpu(gcam * 255)
        gcam = cv2.resize(np.uint8(gcam), (224, 224))

        return gcam


class GuidedBackprop(BaseBackprop):
    def __init__(self, model):
        super(GuidedBackprop, self).__init__(model)
        for key, funcs in model.functions.items():
            for i in range(len(funcs)):
                if funcs[i] is F.relu:
                    funcs[i] = GuidedReLU()

    def generate(self, x, label, layer):
        acts = self.backward(x, label, layer)
        #gbp = chainer.cuda.to_cpu(acts['input'].grad[0])
        gbp = acts['input'].grad[0]
        gbp = gbp.transpose(1, 2, 0)

        return gbp
