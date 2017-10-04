# -*- coding: utf-8 -*-

import arff
import numpy as np

class ARFFBoxLabel:
    """ARFF Box Label Exchange class"""
    def __init__(self):
#        attributes = {u'FileName':0, u'BoxNumber':1, u'BoxCenterX':2, u'BoxCenterY':3, u'BoxWidth':4, u'BoxHeight':5}
        return
    
    def toARFF(self, data, Type=u'MultiBox'):
        obj = self.create(Type)
        for i in range(len(data)):
            obj['data'].append(data[i])
        return obj
    
    def create(self, Type=u'MultiBox'):
        if Type == u'CenterOnly':
            obj = {u'description':u'',
                   u'relation':Type,
                   u'attributes': [
                    (u'FileName', u'STRING'),(u'BoxNumber', u'INTEGER'),
                    (u'BoxCenterX', u'INTEGER'),(u'BoxCenterY', u'INTEGER'),
                   ],
                   u'data': []
                  }
        elif Type == u'MultiBox':
            obj = {u'description':u'',
                   u'relation':Type,
                   u'attributes': [
                    (u'FileName', u'STRING'),(u'BoxNumber', u'INTEGER'),
                    (u'BoxCenterX', u'INTEGER'),(u'BoxCenterY', u'INTEGER'),
                    (u'BoxWidth', u'INTEGER'),(u'BoxHeight', u'INTEGER')
                   ],
                   u'data': []
                  }
        return obj
        
    def read(self, filename):
        obj = arff.load(open(filename, 'rb'))
        return obj
        
    def readCSV(self, filename, attributes, sort):
        f = open(filename, 'r')
        csv = []
        for line in f:
            if line != "\n" and line[0] != '#':
                line = line.split(',')
                data = []
                for i in sort:
                    if attributes[i] == u'INTEGER':
                        data.append(int(line[i]))
                    elif attributes[i] == u'REAL':
                        data.append(float(line[i]))
                    elif attributes[i] == u'STRING':
                        data.append(unicode(line[i]))
                csv.append(data)
        
        f.close()
        return csv
        
    def write(self, obj, filename):
        encoder = arff.ArffEncoder()
        f = open(filename, 'wb')
        f.write(encoder.encode(obj))
        f.close()
        return
        
