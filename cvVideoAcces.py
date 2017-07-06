# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 12:48:05 2017
"""

import cv2
import datetime

class cvVideoAccess:
    def __init__(self):
        self.file = ""
        self.cap = None
        self.writer = None
        return
        
    def __del__(self):
        if self.cap is not None: self.cap.release()
        if self.writer is not None: self.writer.release()
        return

    def open(self, filename):
        self.file = filename
        self.cap = cv2.VideoCapture(filename)
        self.fps = self.cap.get(5) # CV_CAP_PROP_FPS
        self.width = self.cap.get(3) # CV_CAP_PROP_FRAME_WIDTH
        self.height = self.cap.get(4) # CV_CAP_PROP_FRAME_HEIGHT
        self.frames = int(self.cap.get(7)) # CV_CAP_PROP_FRAME_COUNT
        return
        
    def create(self, filename, width, height, fps, fourcc):
        self.file = filename
        self.fourcc = fourcc
        self.width = width
        self.height = height
        self.fps = fps
        self.writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
        return
        
    def set_frame(self, frame, fno):
        self.seek_frame(fno)
        self.set_next(frame)
        return
        
    def set_next(self, frame):
        self.writer.write(frame)
        return

    # 通常 drop frame NTSC系映像ファイルに29.97fpsか59.94などが入っている
    # non drop frameで計算する場合は30か60などを設定する
    def set_fps(self, fps):
        self.fps = fps
        return

    def seek_frame(self, fno):
        self.cap.set( 1, fno) # CV_CAP_PROP_POS_FRAMES
        return
    
    def seek_time(self, d=0, h=0, m=0, s=0, f=0):
        ss = datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)
        fno = int(ss.total_seconds() * self.fps + f)
        self.seek_frame(fno)
        return fno
        
    def get_next(self):
        ret, frame = self.cap.read()
        return ret, frame
        
    def get_frame(self, fno):
        self.seek_frame(fno)
        return self.get_next()
        
    def video_width(self):
        return int(self.width)
        
    def video_height(self):
        return  int(self.height)
        
    def video_fps(self):
        return self.fps
        
    def video_frames(self):
        return self.frames
        
