# -*- coding: utf-8 -*-
"""
Created on Mon Mar 06 17:44:12 2017

@author: User327
"""
import numpy as np

def auc_hq(y, y_pred, pos_label=0):
    from sklearn.metrics import auc
    from sklearn.metrics import roc_curve
    fpr, tpr, thresholds = roc_curve(y, y_pred, pos_label=pos_label)
    sauc = auc(fpr, tpr)
    #from sklearn.metrics import roc_auc_score
    #sauc = roc_auc_score(y, y_pred)
    return(sauc)

def accuracy_hq(y, y_pred, normalize=True):
    from sklearn.metrics import accuracy_score
    sacc = accuracy_score(y, y_pred, normalize=normalize)
    return(sacc)

def recall_hq(y, y_pred, average=None):
    from sklearn.metrics import recall_score
    srec = recall_score(y, y_pred, average=average)
    return(srec)
    
def precision_hq(y, y_pred, average=None):
    from sklearn.metrics import precision_score
    spre = precision_score(y, y_pred, average=average)
    return(spre)

def precision_recall_hq(y, y_pred, pos_label=2):
    from sklearn.metrics import precision_recall_curve
    import operator
    precision, recall, thresholds = precision_recall_curve(y, y_pred, pos_label=pos_label)
    f1 = 2 * (precision * recall)/(precision + recall + 1e-10) #!!!!!
    #min_index, min_value = min(enumerate(values), key=operator.itemgetter(1))
    max_index, max_value = max(enumerate(f1), key=operator.itemgetter(1))
    sthr = thresholds[max(max_index-1,0)]
    return(sthr)
    

    
def allMetrics(y, y_pred, pos_label=0, average=None):
    auc = auc_hq(y,y_pred, pos_label)
    
    sthr = precision_recall_hq(y, y_pred, pos_label)
    ###print sthr
    if pos_label==0:
        nlab = 1
    elif pos_label==1:
        nlab = 0
    yintp = np.array([nlab] * len(y))
    yintp[y_pred >= sthr] = pos_label
    
    accuracy = accuracy_hq(y,yintp)
    recall = recall_hq(y,yintp,average)
    precision = precision_hq(y,yintp,average)
    return(auc, accuracy, recall, precision, sthr)
    

def testMetrics_classifer():
    ## test #### 
    y = np.array([1, 1, 2, 2])
    pred = np.array([0.1, 0.4, 0.35, 0.8])
    print auc_hq(y,pred)

    y_true = [0, 1, 2, 0, 1, 2]
    y_pred = [0, 2, 1, 0, 0, 1]
    print accuracy_hq(y_true,y_pred)
    print recall_hq(y_true,y_pred,'macro')
    print precision_hq(y_true,y_pred,'macro')
    
    auc, accuracy, recall, precision = allMetrics(y, pred, pos_label=2,     average='macro')
    print auc
    print accuracy
    print recall
    print precision


