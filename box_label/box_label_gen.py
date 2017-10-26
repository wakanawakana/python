# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:01:30 2017

@author: 10008777
"""
import cv2
import os
import sys
import re
import numpy as np
import tkMessageBox
from PIL import Image
from PIL import ImageTk
import Tkinter


root = Tkinter.Tk()
tkvar_testno =Tkinter.IntVar(root)
global currimg, itemno, listno, bx, by, bw, bh, bn
labels = []
  
def create_box(img, x, y, w, h, color = (0,0,255), line = 1):
    out = img.copy()
    cv2.rectangle(out, (x,y), (x+w,y+h), color, line)
    return out

def load_list(filepath):
    f = open(filepath, 'r')
    lists = []
    for line in f:
        if line != "\n" and line[0] != '#':
            line = line.rstrip('\n')
            lists.append(line)
    
    f.close()
    return lists

def load_labels(csv, imglist):
    global listno
    if True:
        for no in range(0, len(csv)):
            splitline = csv[no].split(',')
            listno = find_itemno(splitline[0], imglist)
            if listno == -1: continue
            labels.append([listno, int(splitline[1]), int(splitline[4]), int(splitline[5]), int(splitline[6]), int(splitline[7])])
#            labels.append([listno, int(splitline[1]), int(splitline[4])/4, int(splitline[5])/4])

    else:
        itemno = listno = 0
        old = -1
        for no in range(0, len(csv)):
            splitline = csv[no].split(',')
            listno = int(splitline[1])
            if listno != old:
                itemno = 0
            labels.append([listno, itemno, int(splitline[4]), int(splitline[5])])
            itemno += 1
            old = listno
            
    return

def split_cat(lists, cat, delim):
    new_list = []
    for no in range(0, len(lists)):
        split = lists[no].split(delim)
        line = ""
        adddelim = False
        for cn in range(0, len(cat)):
            if cat[cn] == 1:
                if adddelim:
                    line += delim
                line += split[cn]
                adddelim = True

        new_list.append(line)
    return new_list
   
def save_csv(imglists, filepath):
    global labels
    f = open(filepath, 'w')
    for n in range(0, len(labels)):
        l = labels[n][0]
        fname = os.path.basename(imglists[l])
        recode = "{}, {}, {}, {}, {}, {}, {}, {}\n".format(fname, labels[n][1], 0, 0, labels[n][2], labels[n][3], labels[n][4], labels[n][5])
        f.write(recode)
    return
    
def test_exit(imglists):
    save_csv(imglists, "./gen_box.csv")
    sys.exit()
    return
   
def label_setimg(label, imgin):
    img = cv2.cvtColor(imgin, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)
    label.configure(image=img)
    label.image = img    
    return

    
def key_bind_n(label, topdir, mlists, imglists):
    print "evnet"
    return

def find_label_entry(no):
    ret = 0
    for n in range(0, len(labels)):
        if labels[n][0] == no:
            ret += 1
    return ret

def find_itemno(test, imglist):
    for n in range(0, len(imglist)):
        fname = os.path.basename(imglist[n])
        if test == fname: return n
    return -1
            
def img_next(label, topdir, imglists, button):
    global currimg, listno, itemno
    listno += 1
    if listno > len(imglists): listno = len(imglists)
    itemno = find_label_entry(listno)
    fpath = os.path.join(topdir, imglists[listno])
    currimg = cv2.imread(fpath)
    img = curr_labels_boximg(listno, currimg)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def img_back(label, topdir, imglists, button):
    global currimg, listno, itemno
    listno -= 1
    if listno < 0: listno = 0
    itemno = find_label_entry(listno)
    fpath = os.path.join(topdir, imglists[listno])
    currimg = cv2.imread(fpath)
    img = curr_labels_boximg(listno, currimg)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def center_l(event, label, listno, button):
    global labels, bx, by, bw, bh
    bx -= 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def center_r(event, label, listno, button):
    global labels, bx, by, bw, bh
    bx += 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def center_u(event, label, listno, button):
    global labels, bx, by, bw, bh
    by -= 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def center_b(event, label, listno, button):
    global labels, bx, by, bw, bh
    by += 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    return
    
def wide_lr(event, label, listno, button):
    global labels, bx, by, bw, bh
    bw += 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    return
    
def short_lr(event, label, listno, button):
    global labels, bx, by, bw, bh
    bw -= 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def wide_ub(event, label, listno, button):
    global labels, bx, by, bw, bh
    bh += 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    return
    
def short_ub(event, label, listno, button):
    global labels, bx, by, bw, bh
    bh -= 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def click_left(event, label, listno, button):
    global labels, bx, by, bw, bh
    print "click", event.x, event.y
    bx = event.x
    by = event.y
    bw = bh = 30
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - 15, by - 15, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def click_right(event, label, listno, button):
    global labels, bx, by, bw, bh
    print "click", event.x, event.y
    bw = event.x - bx
    bh = event.y - by
    print "w:h", bw, bh
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx, by, bw, bh)
    label_setimg(label, img)
    button.config(state="disabled")
    bx = bx + bw/2
    by = by + bh/2
    return
    
def curr_labels_boximg(no, img):
    for n in range(0, len(labels)):
        if labels[n][0] == no:
            img = create_box(img, labels[n][2] - labels[n][4]/2, labels[n][3] - labels[n][5]/2, labels[n][4], labels[n][5], color=(0,255,0))
    return img
    
def box_add(label, listno, bx, by, bw, bh):
    global itemno
    labels.append([listno, itemno, bx, by, bw, bh])
    img = curr_labels_boximg(listno, currimg)
    label_setimg(label, img)
    itemno += 1
    return

def boxsel(label, button):
    global labels, currimg, listno, itemno, bn
    bn += 1
    if bn > itemno - 1: bn = 0
    img = currimg.copy()
    for n in range(0, len(labels)):
        if labels[n][0] == listno:
            if labels[n][1] == bn:
                img = create_box(img, labels[n][2]- labels[n][4]/2, labels[n][3]-labels[n][5]/2, labels[n][4], labels[n][5], color=(0,0,255))
            else:
                img = create_box(img, labels[n][2]-labels[n][4]/2, labels[n][3]-labels[n][5]/2, labels[n][4], labels[n][5], color=(0,255,0))
    label_setimg(label, img)
    button.config(state="normal")
    return

def boxdel(label, button):
    global labels, currimg, listno, itemno
    for n in range(0, len(labels)):
        if labels[n][0] == listno:
            if labels[n][1] == bn:
                labels.pop(n)
                
    itemno = find_label_entry(listno)
    img = curr_labels_boximg(listno, currimg, 30, 30)
    label_setimg(label, img)
    button.config(state="disabled")
    return 

def create_cls_window(root, topdir, imglists):
    global currimg, itemno, listno, bx, by, bw, bh, bs
    mainframe = Tkinter.Frame(root)
    mainframe.grid(column=0,row=0, sticky=(Tkinter.N,Tkinter.W,Tkinter.E,Tkinter.S) )
#    mainframe.columnconfigure(1, weight = 0)
#    mainframe.rowconfigure(1, weight = 0)
    mainframe.pack(pady = 10, padx = 10)
    # Create a Tkinter variable
    tkvar_testno.set(0)

    label = Tkinter.Label(mainframe, borderwidth=0)
    label.grid(row = 1, column =1)
    fpath = os.path.join(topdir, imglists[listno])
    currimg = cv2.imread(fpath)
    img = curr_labels_boximg(listno, currimg)
    label_setimg(label, img)
    itemno = find_label_entry(listno)

    button12 = Tkinter.Button(mainframe, text = '□', command = lambda: boxsel(label, button13))
    button12.grid(row=1,column=2)
    button13 = Tkinter.Button(mainframe, text = '□Del', command = lambda: boxdel(label, button13))
    button13.grid(row=1,column=3)
    button13.config(state="disabled")
    button32 = Tkinter.Button(mainframe, text = 'Next', command = lambda: img_next(label, topdir, imglists, button13))
    button32.grid(row=3,column=2)
    button33 = Tkinter.Button(mainframe, text = 'Back', command = lambda: img_back(label, topdir, imglists, button13))
    button33.grid(row=3,column=3)
    button34 = Tkinter.Button(mainframe, text = 'Add(a)', command = lambda: box_add(label, listno, bx, by, bw, bh))
    button34.grid(row=3,column=4)
    button35 = Tkinter.Button(mainframe, text = 'Exit', command = lambda: test_exit(imglists))
    button35.grid(row=3,column=5)
    label.bind("<Button-1>", lambda e: click_left(e, label, listno, button13))
    root.bind('a', lambda e: box_add(label, listno, bx, by, bw, bh))
    root.bind("<Button-3>", lambda e: click_right(e, label, listno, button13))
    root.bind('6', lambda e: wide_lr(e, label, listno, button13))
    root.bind('4', lambda e: short_lr(e, label, listno, button13))
    root.bind('8', lambda e: wide_ub(e, label, listno, button13))
    root.bind('2', lambda e: short_ub(e, label, listno, button13))
    root.bind('<Right>', lambda e: center_r(e, label, listno, button13))
    root.bind('<Left>', lambda e: center_l(e, label, listno, button13))
    root.bind('<Up>', lambda e: center_u(e, label, listno, button13))
    root.bind('<Down>', lambda e: center_b(e, label, listno, button13))
    root.mainloop()
    return
   
if __name__ == '__main__':
    global itemno, listno, bn
    root.title("box label maker")
    topdir = "./images"
    itemno = listno = bn = 0

    imglist = sys.argv[1]
    imglist = load_list(imglist)
    if len(sys.argv) > 2:
        csvfile = sys.argv[2]
        csv = load_list(csvfile)
        load_labels(csv, imglist)

    create_cls_window(root, topdir, imglist)
    
