# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:23:54 2017
"""

import sys
import subprocess


def train(cmd, log):
    try :
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            line = proc.stdout.readline()
            sys.stdout.write(line)
            log.write(line)
            if proc.poll() is not None:
                break
    
    except KeyboardInterrupt:
        print "aborted"
        proc.kill()
        line, serr = proc.communicate()
        log.write(line)
    
    log.close()
    return

if __name__ == '__main__':
    cmd = ['/home/darknet/darknet', 'detector', 'train', './cfg/yolo.data', './cfg/yolo.cfg']
    log = open('./train_log.txt', 'w')
    if len(sys.argv) > 2:
        cmd[3] = sys.argv[1]
        cmd[4] = sys.argv[2]
    train(cmd, log)

