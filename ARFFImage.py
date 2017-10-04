# -*- coding: utf-8 -*-

import arff
import numpy as np

class ARFFImage:
    """ARFF Image Exchange class"""
    def __init__(self):
        return
    
    def toARFF(self, image, Type=u'GrayImage'):
        if image.shape[2] == 1:
            if Type == u'MaskImage':
                obj = {u'description':u'',
                       u'relation':Type,
                       u'attributes': [
                        (u'x', u'INTEGER'),(u'y', u'INTEGER'),
                       ],
                       u'data': []
                      }
                for y in range(image.shape[0]):
                    for x in range(image.shape[1]):
                        obj['data'].append([x, y])
            elif Type == u'GrayImage':
                obj = {u'description':u'',
                       u'relation':Type,
                       u'attributes': [
                        (u'x', u'INTEGER'),(u'y', u'INTEGER'),(u'gray', u'INTEGER')
                       ],
                       u'data': []
                      }
                for y in range(image.shape[0]):
                    for x in range(image.shape[1]):
                        obj['data'].append([x, y, image[y,x,0]])                
        elif image.shape[2] == 3:
            obj = {u'description':u'',
                   u'relation':u'RGBImage',
                   u'attributes': [
                    (u'x', u'INTEGER'), (u'y', u'INTEGER'), (u'b', u'INTEGER'), (u'g', u'INTEGER'), (u'r', u'INTEGER')
                   ],
                   u'data': []
                  }
            for y in range(image.shape[0]):
                for x in range(image.shape[1]):
                    obj['data'].append([x, y, image[y,x,0], image[y,x,1], image[y,x,2]])

        elif image.shape[2] == 4:
            obj = {u'description':u'',
                   u'relation':u'RGBAImage',
                   u'attributes': [
                    (u'x', u'INTEGER'), (u'y', u'INTEGER'), (u'b', u'INTEGER'), (u'g', u'INTEGER'), (u'r', u'INTEGER'), (u'a', u'INTEGER')
                   ],
                   u'data': []
                  }
            for y in range(image.shape[0]):
                for x in range(image.shape[1]):
                    obj['data'].append([x, y, image[y,x,0], image[y,x,1], image[y,x,2], image[y,x,3]])

        return obj
    
    def toMask(self, obj, width, height):
        '''
        @RELATION  ImageMask
        @ATTRIBUTE x integer
        @ATTRIBUTE y integer
        '''
        img = np.zeros((width, height, 1), np.uint8)
        for i in range(0, len(obj['data'])):
            img[obj['data'][i][0], obj['data'][i][1]] = 255
        return img

    def toImage(self, obj):
        # support @RELATION  MaskImage, GrayImage, RGBImage, RGBAImage 
        width = height = 0
        for i in range(len(obj['data'])):
            width = max(width, obj['data'][i][0])
            height = max(height, obj['data'][i][1])
        width += 1
        height += 1
        if obj['relation'] == u'GrayImage':
            img = np.zeros((height, width, 1), np.uint8)
            for i in range(0, len(obj['data'])):
                img[obj['data'][i][1], obj['data'][i][0]] = [obj['data'][i][2]]
        if obj['relation'] == u'MaskImage':
            img = np.zeros((height, width, 1), np.uint8)
            for i in range(0, len(obj['data'])):
                img[obj['data'][i][1], obj['data'][i][0]] = [255]
        elif obj['relation'] == u'RGBImage':
            img = np.zeros((height, width, 3), np.uint8)
            for i in range(0, len(obj['data'])):
                img[obj['data'][i][1], obj['data'][i][0]] = [obj['data'][i][2], obj['data'][i][3], obj['data'][i][4]]
        elif obj['relation'] == u'RGBAImage':
            img = np.zeros((width, height, 4), np.uint8)
            for i in range(0, len(obj['data'])):
                img[obj['data'][i][1], obj['data'][i][0]] = [obj['data'][i][2], obj['data'][i][3], obj['data'][i][4], obj['data'][i][5]]

        return img

    def read(self, filename):
        obj = arff.load(open(filename, 'rb'))
        return obj
        
    def write(self, obj, filename):
        encoder = arff.ArffEncoder()
        f = open(filename, 'wb')
        f.write(encoder.encode(obj))
        f.close()
        return
        
