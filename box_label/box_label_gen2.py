# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:01:30 2017

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
import tkFileDialog

root = Tkinter.Tk()
tkvar_testno =Tkinter.IntVar(root)
global currimg, itemno, listno, bx, by, bw, bh, bxc, byc, bn, tip, tipx, tipy
labels = []

def tip2cord(xc, yc, w, h, tip):
    global tipx, tipy
    if tip == 0:
        tx = xc - w/2
        ty = yc - h/2
    elif tip == 1:
        tx = xc + w/2
        ty = yc - h/2
    elif tip == 2:            
        tx = xc + w/2
        ty = yc + h/2
    elif tip == 3:    
        tx = xc - w/2
        ty = yc + h/2
    else:
        tx = tipx
        ty = tipy
    return tx, ty
    
def draw_star(img, x, y):
    cv2.circle(img, (x, y), 6, (0, 255, 0), 1);
    return img
    
def create_box(img, x, y, w, h, tx, ty, color = (0,0,255), line = 1):
    out = img.copy()
    cv2.rectangle(out, (x,y), (x+w,y+h), color, line)
    cv2.line(out, (x+w/2,y), (x+w/2,y+h), color, line) # + guide
    cv2.line(out, (x,y+h/2), (x+w,y+h/2), color, line) # + guide
    x1 = tx
    y1 = ty
    x2 = x+w/2
    y2 = y+h/2
    grad = float(y2 - y1) / float(x2 - x1)
    if x1 < x2:
        cv2.line(out, (tx,ty), (x+w, int(grad*(x+w-x1)+y1)), color, line) # vec guide
    else:
        cv2.line(out, (x, int(grad*(x-x1)+y1)), (tx,ty), color, line) # vec guide
    out = draw_star(out, tx, ty )
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
            labels.append([listno, int(splitline[1]), int(splitline[2]), int(splitline[3]), int(splitline[4]), int(splitline[5]), int(splitline[6]), int(splitline[7]), int(splitline[8])])
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
        recode = "{}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(fname, labels[n][1], labels[n][2], labels[n][3], labels[n][4], labels[n][5], labels[n][6], labels[n][7], labels[n][8])
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
    global labels, bxc, byc, bw, bh, tipx, tipy
    bxc -= 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bxc - bw/2, byc - bh/2, bw, bh, tipx, tipy)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def center_r(event, label, listno, button):
    global labels, bxc, byc, bw, bh, tipx, tipy
    bxc += 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bxc - bw/2, byc - bh/2, bw, bh, tipx, tipy)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def center_u(event, label, listno, button):
    global labels, bxc, byc, bw, bh, tipx, tipy
    byc -= 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bxc - bw/2, byc - bh/2, bw, bh, tipx, tipy)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def center_b(event, label, listno, button):
    global labels, bxc, byc, bw, bh, tipx, tipy
    byc += 1
    img = curr_labels_boximg(listno, currimg)
    tx, ty = tip2cord(bx, by, bw, bh, tip)
    img = create_box(img, bxc - bw/2, byc - bh/2, bw, bh, tx, ty)
    label_setimg(label, img)
    button.config(state="disabled")
    return
    
def wide_lr(event, label, listno, button):
    global labels, bxc, byc, bw, bh, tipx, tipy
    bw += 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bxc - bw/2, byc - bh/2, bw, bh, tipx, tipy)
    label_setimg(label, img)
    button.config(state="disabled")
    return
    
def short_lr(event, label, listno, button):
    global labels, bx, by, bw, bh, tipx, tipy
    bw -= 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bxc - bw/2, byc - bh/2, bw, bh, tipx, tipy)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def wide_ub(event, label, listno, button):
    global labels, bxc, byc, bw, bh, tipx, tipy
    bh += 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bxc - bw/2, byc - bh/2, bw, bh, tipx, tipy)
    label_setimg(label, img)
    button.config(state="disabled")
    return
    
def short_ub(event, label, listno, button):
    global labels, bxc, byc, bw, bh, tipx, tipy
    bh -= 1
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bxc - bw/2, byc - bh/2, bw, bh, tipx, tipy)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def click_left(event, label, listno, button):
    global labels, bx, by, bw, bh, bxc, byc, tipx, tipy
    print "click", event.x, event.y
    bx = event.x
    by = event.y
    bw = bh = 30
    bxc = bx
    byc = by
    img = curr_labels_boximg(listno, currimg)
    tipx, tipy = tip2cord(bxc, byc, bw, bh, tip)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh, tipx, tipy)
    label_setimg(label, img)
    button.config(state="disabled")
    return

def click_right(event, label, listno, button):
    global labels, bx, by, bw, bh, bxc, byc, tipx, tipy
    print "click", event.x, event.y
    if event.x != bx and event.y != by:
        bw = event.x - bx
        bh = event.y - by
        bxc = bx + bw/2
        byc = by + bh/2
        print "w:h", bw, bh
        img = curr_labels_boximg(listno, currimg)
        img = create_box(img, bxc - bw/2, byc - bh/2, bw, bh, tipx, tipy)
        label_setimg(label, img)
        button.config(state="disabled")
        tip = 0
    return
    
def curr_labels_boximg(no, img):
    for n in range(0, len(labels)):
        if labels[n][0] == no:
            img = create_box(img, labels[n][2] - labels[n][4]/2, labels[n][3] - labels[n][5]/2, labels[n][4], labels[n][5], labels[n][6], labels[n][7], color=(0,255,0))
    return img
    
def box_add(label, listno, bxc, byc, bw, bh):
    global itemno, tip
    labels.append([listno, itemno, bxc, byc, bw, bh, tipx, tipy, tip])
    img = curr_labels_boximg(listno, currimg)
    label_setimg(label, img)
    itemno += 1
    return

def tip_set(event, label, listno):
    global tipx, tipy, tip, bxc, byc
    print "center click", event.x, event.y
    tipx = event.x
    tipy = event.y
    tip = 4
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx, by, bw, bh, tipx, tipy)
    label_setimg(label, img)
    return

def boxsel(label, button):
    global labels, currimg, listno, itemno, bn, tip
    bn += 1
    if bn > itemno - 1: bn = 0
    img = currimg.copy()
    for n in range(0, len(labels)):
        if labels[n][0] == listno:
            if labels[n][1] == bn:
                img = create_box(img, labels[n][2]- labels[n][4]/2, labels[n][3]-labels[n][5]/2, labels[n][4], labels[n][5], labels[n][6], labels[n][7], color=(0,0,255))
            else:
                img = create_box(img, labels[n][2]-labels[n][4]/2, labels[n][3]-labels[n][5]/2, labels[n][4], labels[n][5], labels[n][6], labels[n][7], color=(0,255,0))
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

def settip(label, button):
    global tip
    tip += 1
    if tip > 3:
        tip = 0
    img = curr_labels_boximg(listno, currimg)
    img = create_box(img, bx - bw/2, by - bh/2, bw, bh, tip)
    label_setimg(label, img)
    return

def create_cls_window(root, topdir, imglists):
    global currimg, itemno, listno, bx, by, bxc, byc, bw, bh, bs, tip
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
    tip = 0

    button12 = Tkinter.Button(mainframe, text = '□', command = lambda: boxsel(label, button13))
    button12.grid(row=1,column=2)
    button13 = Tkinter.Button(mainframe, text = '□Del', command = lambda: boxdel(label, button13))
    button13.grid(row=1,column=3)
    button13.config(state="disabled")
#    button14 = Tkinter.Button(mainframe, text = '*', command = lambda: settip(label, button13))
#    button14.grid(row=1,column=4)
    button32 = Tkinter.Button(mainframe, text = 'Next', command = lambda: img_next(label, topdir, imglists, button13))
    button32.grid(row=3,column=2)
    button33 = Tkinter.Button(mainframe, text = 'Back', command = lambda: img_back(label, topdir, imglists, button13))
    button33.grid(row=3,column=3)
    button34 = Tkinter.Button(mainframe, text = 'Add(a)', command = lambda: box_add(label, listno, bxc, byc, bw, bh))
    button34.grid(row=3,column=4)
    button35 = Tkinter.Button(mainframe, text = 'Exit', command = lambda: test_exit(imglists))
    button35.grid(row=3,column=5)
    label.bind("<Button-1>", lambda e: click_left(e, label, listno, button13))
    root.bind('<Button-2>', lambda e: tip_set(e, label, listno))
    root.bind('a', lambda e: box_add(label, listno, bx, by, bw, bh))
    root.bind("<Button-3>", lambda e: click_right(e, label, listno, button13))
#    root.bind("<ButtonRelease-1>", lambda e: click_right(e, label, listno, button13))
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
    csvfile = ''

    imglist = sys.argv[1]
    imglist = load_list(imglist)
    if len(sys.argv) > 2:
        csvfile = sys.argv[2]
    else:
        csvfile = tkFileDialog.askopenfilename(title='BOXファイル読み込み', filetypes=[('csvファイル','*.csv')],initialfile='gen_box.csv')

    if csvfile != '':
        csv = load_list(csvfile)
        load_labels(csv, imglist)

    create_cls_window(root, topdir, imglist)
    
