# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:23:54 2017
"""

import re
import matplotlib.pyplot as plt
import numpy as np

def subprot(bs, Loss, Iou, LR, Rec, Obj, NObj):
    loss = np.array(Loss)
    iou = np.array(Iou)
    lr = np.array(LR)
    rec = np.array(Rec)
    obj = np.array(Obj)
    nobj = np.array(NObj)
    
    loss_x = np.arange(1, len(Loss) + 1, 1)
    iou_x = np.arange(1, len(Iou) + 1, 1)
    fig = plt.figure(figsize=(16,10))
    ax1 = fig.add_subplot(231)
    ax1.plot(loss_x, loss)
#    ax1.set_ylim(0, 3)
    ax1.set_ylabel('Loss(avg)')
    ax1.set_xlabel('Batch({})'.format(bs))
    ax1.set_yscale('log')
    ax1.grid(True)
    
    ax2 = fig.add_subplot(232)
    ax2.plot(iou_x, iou)
    ax2.set_ylim(0, 1)
    ax2.set_ylabel('IOU(subdiv)')
    ax2.set_xlabel('Batch(x subdiv)')
    ax2.grid(True)

    ax3 = fig.add_subplot(233)
    ax3.plot(iou_x, rec)
    ax3.set_ylim(0, 1)
    ax3.set_ylabel('Recall(subdiv)')
    ax3.set_xlabel('Batch(x subdiv)')
    ax3.grid(True)
    
    ax4 = fig.add_subplot(234)
    ax4.plot(loss_x, lr)
    ax4.set_ylim(0, 0.0011)
    ax4.set_ylabel('Learning Rate')
    ax4.grid(True)
#    ax4.set_yscale('log')

    ax5 = fig.add_subplot(235)
    ax5.plot(iou_x, obj)
    ax5.set_ylim(0, 1)
    ax5.set_ylabel('Obj')
    ax5.grid(True)

    ax6 = fig.add_subplot(236)
    ax6.plot(iou_x, nobj)
    ax6.set_ylim(0, 0.1)
    ax6.set_ylabel('NoObj')
    ax6.grid(True)
    
    plt.show()
    return

def prot(loss):
    la = np.array(loss)
    plt.plot(la)
    plt.ylabel('loss')
    plt.show()
    return
    
def collect_loss(log, loss):
    for n in range(0, len(log)):
        line = log[n]
        match = re.search("^\d{1,}:", line)
        if match != None:
            p1 = line.find(',') + 2
            p2 = p1 + line[p1:].find(' ')
            try:
                num = float(line[p1:p2])
            except:
                num = 0.0
            loss.append(num)
    return loss

def collect_iou(log, iou):
    for n in range(0, len(log)):
        line = log[n]
        match = re.search("^Region Avg IOU:", line)
        if match != None:
            p1 = line.find(' ') + 1
            p1 += line[p1:].find(' ') + 1
            p1 += line[p1:].find(' ') + 1
            p2 = line.find(',')
            try:
                num = float(line[p1:p2])
            except:
                num = iou[len(iou) - 1]
            iou.append(num)
    return iou

def collect_lr(log, lr):
    for n in range(0, len(log)):
        line = log[n]
        match = re.search("^\d{1,}:", line)
        if match != None:
            p1 = line.find('avg') + 5
            p2 = p1 + line[p1:].find(' ')
            try:
                num = float(line[p1:p2])
            except:
                num = lr[len(lr) - 1]
            lr.append(num)
    return lr

def collect_recall(log, rec):
    for n in range(0, len(log)):
        line = log[n]
        match = re.search("^Region Avg IOU:", line)
        if match != None:
            p1 = line.find('Recall') + 8
            p2 = p1 + line[p1:].find(',')
            try:
                num = float(line[p1:p2])
            except:
                num = rec[len(rec) - 1]
            rec.append(num)
    return rec

def collect_obj(log, obj):
    for n in range(0, len(log)):
        line = log[n]
        match = re.search("^Region Avg IOU:", line)
        if match != None:
            p1 = line.find('Obj') + 5
            p2 = p1 + line[p1:].find(',')
            try:
                num = float(line[p1:p2])
            except:
                num = obj[len(obj) - 1]
            obj.append(num)
    return obj

def collect_nobj(log, nobj):
    for n in range(0, len(log)):
        line = log[n]
        match = re.search("^Region Avg IOU:", line)
        if match != None:
            p1 = line.find('No Obj') + 8
            p2 = p1 + line[p1:].find(',')
            try:
                num = float(line[p1:p2])
            except:
                num = nobj[len(nobj) - 1]
            nobj.append(num)
    return nobj

def load_list(filepath):
    f = open(filepath, 'r')
    lists = []
    for line in f:
        if line != "\n" and line[0] != '#':
            line = line.rstrip('\n')
            lists.append(line)
    
    f.close()
    return lists
    
if __name__ == '__main__':
    loss = []
    iou = []
    lr = []
    rec = []
    obj = []
    nobj = []
    log = load_list("../wakanawakana/win-darknet/train_log.txt")
    loss = collect_loss(log, loss)
    iou = collect_iou(log, iou)
    lr = collect_lr(log, lr)
    rec = collect_recall(log, rec)
    obj = collect_obj(log, obj)
    nobj = collect_nobj(log, nobj)
    subprot(8, loss, iou, lr, rec, obj, nobj)
