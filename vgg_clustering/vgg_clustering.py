#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Used with chainer-imagenet-vgg
#  https://github.com/mitmul/chainer-imagenet-vgg

import argparse
import numpy as np
import cv2 as cv
import cPickle as pickle
from VGGNet import VGGNet
from chainer import cuda
from chainer import serializers
from sklearn.cluster import KMeans
from sklearn.decomposition import RandomizedPCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
#from pyclustering.cluster.kmeans import kmeans
#from pyclustering.cluster.xmeans import xmeans, splitting_type
#from pyclustering.cluster import cluster_visualizer
#from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES
#from pyclustering.utils import read_sample

def extract_features(vgg, img):
    if args.gpu >= 0:
        img = cuda.cupy.asarray(img, dtype=np.float32)
    temp = vgg.extract(img, layers=['fc7', 'prob'])
    if args.gpu >= 0:
        fc7 = cuda.to_cpu(temp['fc7'].data)
        prob = cuda.to_cpu(temp['prob'].data)
    else:
        fc7 = temp['fc7'].data
        prob = temp['prob'].data
    return fc7, prob
  
def prepare_img(path):
    mean = np.array([103.939, 116.779, 123.68])
    img = cv.imread(path).astype(np.float32)
#    img = cv.imread("images/dog.jpg").astype(np.float32)
    img -= mean
    img = cv.resize(img, (224, 224)).transpose((2, 0, 1))
    img = img[np.newaxis, :, :, :]
    return img  
    
def prob_name(pred, path, no):
    words = open('data/synset_words.txt').readlines()
    words = [(w[0], ' '.join(w[1:])) for w in [w.split() for w in words]]
    words = np.asarray(words)

    top5 = np.argsort(pred)[0][::-1][:3]
    probs = np.sort(pred)[0][::-1][:5]
    print no, path[no]
    for w, p in zip(words[top5], probs):
        print('\t{}\tprobability:{}'.format(w, p))    

def correct_list_features(flist, vgg, features):
    for i in range(0, len(flist)):
        img = prepare_img(flist[i])
        fc7, prob = extract_features(vgg, img)
        features.append(fc7[0])
        prob_name(prob, flist, i)
    return features

def cat0dog1(flist):
    catdog = []
    for i in range(0, len(flist)):
        if flist[i].find('dog') > -1:
            catdog.append(1)
        else:
            catdog.append(0)
    return catdog

def shochigu(flist):
    shochigu = []
    for i in range(0, len(flist)):
        if flist[i].find('011f') > -1:
            shochigu.append(0)
        elif flist[i].find('012f') > -1:
            shochigu.append(1)
        elif flist[i].find('81a0') > -1:
            shochigu.append(2)
        elif flist[i].find('doc164234') > -1:    
            shochigu.append(3)
        elif flist[i].find('har-tip') > -1:    
            shochigu.append(4)
    return shochigu

if __name__ == '__main__':
    features = []
    features2 = []
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=int, default=0)
    parser.add_argument('--cluster', type=int, default=5)
    args = parser.parse_args()

    vgg = VGGNet()
    serializers.load_hdf5('Train.model', vgg)
    if args.gpu >= 0:
        cuda.get_device(args.gpu)
        vgg.to_gpu()

    
    flist = glob.glob("./Images/*.jpg")
    features = correct_list_features(flist, vgg, features)
    ans = shochigu(flist)
    #ans = cat0dog1(flist)

    model = KMeans(n_clusters=args.cluster, random_state=0)
    labels = model.fit_predict(features)
    length = model.transform(features)
    centers = model.cluster_centers_
    s_len = model.transform(centers)
    print labels
    print ans
    plt.figure(1)
    plt.scatter(length[:, 0], length[:, 1], s=50, c=labels)
    plt.scatter(s_len[:, 0], s_len[:, 1], c='black', s=200, alpha=0.5)
#    for i in range(0,len(length)):
#        plt.annotate("{}".format(i), (length[i][0], length[i][1]))

#    model = Isomap(n_neighbors=args.cluster, n_components=2)
#    length = model.fit_transform(features)
    plt.figure(2)
    plt.scatter(length[:, 0], length[:, 1], s=50, c=ans)
#    for i in range(0,len(length)):
#        plt.annotate("{}".format(i), (length[i][0], length[i][1]))

    
    model = TSNE(n_components=args.cluster, random_state=0)
    X = model.fit_transform(features)
    plt.figure(3)
    plt.scatter(X[:, 0], X[:, 1], c=ans)
    for i in range(0,len(length)):
        plt.annotate("{}".format(i), (X[i][0], X[i][1]))
    
    #model = RandomizedPCA(n_components=3)
    #model = Isomap(n_neighbors=8, n_components=3)
    model = TSNE(n_components=3, random_state=0)
    X = model.fit_transform(features)
    fig = plt.figure(4)
    ax = Axes3D(fig)
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=ans)
    #ax.scatter3D(X[:, 0], X[:, 1], X[:, 2])
    #for i in range(0,len(length)):
       #ax.text(X[i][0], X[i][1], X[i][2], "{}".format(i), 'x')
    plt.show()   
    
    '''
    #xmeans_instance = xmeans(sample, None, 20, tolerane = 0.025, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore = False)
    xmeans_instance.process()
    clusters = xmeans_instance.get_clusters()
    centers = xmeans_instance.get_centers()
    criterion_string = "UNKNOWN"

    visualizer = cluster_visualizer()
    visualizer.set_canvas_title(criterion_string)
    visualizer.append_clusters(clusters, None)
    visualizer.append_cluster(centers, None, marker = '*')
    visualizer.show()
    '''
    
