# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 13:44:58 2017
"""
import os
import re
import sys
import shutil

def load_list(filepath):
    f = open(filepath, 'r')
    lists = []
    for line in f:
        if line != "\n" and line[0] != '#':
            line = line.rstrip('\n')
            lists.append(line)
    
    f.close()
    return lists

def gen_labels(tiplist, name_top, dname, imgw=338.0, imgh=270.0):
    label = "labels"
    
    for no in range(0, len(tiplist)):
        line = tiplist[no]
        line  = name_top + line.replace("_polypmask.png", ".png")
        line = line.split(",")
        curdir = os.getcwd()
        name = os.path.join(curdir, label)
        name = os.path.join(name, dname)
        filename = os.path.join(name, line[0])
        dirname = os.path.dirname(filename)

        if( False == os.path.exists(dirname) ):
            os.makedirs(dirname)

        filename = filename.replace("png", "txt")
        boxtxt = open(os.path.join(dirname, filename), "a")

        x = float(line[4])
        y = float(line[5])
        w = 30.0/imgw
        h = 30.0/imgh
        if x <= 0:
            print "warning value x {} {}".format(filename, x)
            x = 1.0
        if x > imgw:
            print "warning value x {} {}".format(filename, x)
            x = imgw
        if y <= 0:
            print "warning value y {} {}".format(filename, y)
            y = 1.0
        if y > imgh:
            print "warning value y {} {}".format(filename, y)
            y = imgh
        x = x/imgw
        y = y/imgh
        if (x + w/2.0) > 1.0:
            w = w + (1.0 - x - w/2.0)
        if (y + h/2.0) > 1.0:
            h = h + (1.0 - y - h/2.0)
        info = "{0} {1:f} {2:f} {3:f} {4:f}\n".format(1, x, y, w, h)
        boxtxt.write(info)
        boxtxt.close()
        
    return


if __name__ == '__main__':
    labeldir = "./labels"

    # remove old files
   if( True == os.path.exists(labeldir) ):
        shutil.rmtree(labeldir)
    if( True == os.path.exists(trainname) ):
        os.remove(trainname)
    
    top_name = ""
    dname = "A"
    boxlist = load_list("box.csv")

    # gen yolo train labels
    gen_labels(boxlist, top_name, dname)
 
