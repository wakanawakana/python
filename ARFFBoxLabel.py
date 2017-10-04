# -*- coding: utf-8 -*-

import arff
import numpy as np

class ARFFBoxLabel:
    """ARFF Box Label Exchange class"""
    def __init__(self):
#        attributes = {u'FileName':0, u'BoxNumber':1, u'BoxCenterX':2, u'BoxCenterY':3, u'BoxWidth':4, u'BoxHeight':5}
        return
    
    def toARFF(self, data, Type=u'MBMC'):
        obj = self.create(Type)
        for i in range(len(data)):
            obj['data'].append(data[i])
        return obj
    
    def create(self, Type=u'MBMC'):
        if Type == u'CenterOnly':
            obj = {u'description':u'',
                   u'relation':Type,
                   u'attributes': [
                    (u'FileName', u'STRING'),(u'BoxNumber', u'INTEGER'),
                    (u'BoxCenterX', u'INTEGER'),(u'BoxCenterY', u'INTEGER'),
                   ],
                   u'data': []
                  }
        elif Type == u'MBMC':
            obj = {u'description':u'',
                   u'relation':Type,
                   u'attributes': [
                    (u'FileName', u'STRING'),(u'BoxNumber', u'INTEGER'),(u'Class', u'INTEGER'),
                    (u'BoxCenterX', u'INTEGER'),(u'BoxCenterY', u'INTEGER'),
                    (u'BoxWidth', u'INTEGER'),(u'BoxHeight', u'INTEGER')
                   ],
                   u'data': []
                  }
        elif Type == u'MBMCwGrav':
            obj = {u'description':u'',
                   u'relation':Type,
                   u'attributes': [
                    (u'FileName', u'STRING'),(u'BoxNumber', u'INTEGER'),(u'Class', u'INTEGER'),
                    (u'BoxCenterX', u'INTEGER'),(u'BoxCenterY', u'INTEGER'),
                    (u'BoxWidth', u'INTEGER'),(u'BoxHeight', u'INTEGER'),
                    (u'ObjGravityX', u'INTEGER'),(u'ObjGravityY', u'INTEGER')
                   ],
                   u'data': []
                  }
        return obj

    def concat(self, obj1, obj2):
        obj = self.create(obj1['relation'])
        for i in range(len(obj1['data'])): obj['data'].append(obj1['data'][i])
        for i in range(len(obj2['data'])): obj['data'].append(obj2['data'][i])
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
                # Extend data length
                while(len(line) < len(sort)):
                    line.append(0)
                data = []
                for i in sort:
                    if attributes[i] == u'INTEGER':
                        try:
                            data.append(int(line[i]))
                        except:
                            data.append(int(0))
                    elif attributes[i] == u'REAL':
                        try:
                            data.append(float(line[i]))
                        except:
                            data.append(float(0))
                    elif attributes[i] == u'STRING':
                        try:
                            data.append(unicode(line[i]))
                        except:
                            data.append('')
                csv.append(data)
        
        f.close()
        return csv
        
    def write(self, obj, filename):
        encoder = arff.ArffEncoder()
        f = open(filename, 'wb')
        f.write(encoder.encode(obj))
        f.close()
        return
        

