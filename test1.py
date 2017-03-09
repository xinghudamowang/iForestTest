# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 14:36:37 2017

@author: User327
"""

### outside functions
from test_data1 import *
from featureSelect1 import *
from isolation_score import *
from metrics_classifer import *

### inside tool functions
from plotfs import *
import timeit


## data prepare ========================================


## customer filter ========================================


## got simulation data ========================================
x0, y0, x1, y1 = test_data1()
print "Training sample size is  %d, %d" % (x0.shape[0], x0.shape[1])
#print [y0.tolist().count(0), y0.tolist().count(1)]
#print [y1.tolist().count(0), y1.tolist().count(1)]
       
       
## feature selection ========================================
"""
t1= timeit.default_timer()
subs = Ridge_hq(x0, y0)
t2 = timeit.default_timer()
print "Feature selection running time is: %f" % (t2-t1)
plotHist(subs)
cut= 0.0035
fsub = abs(subs) > cut
"""

t1= timeit.default_timer()
fsub = linearCoe_hq(x0, y0)
t2 = timeit.default_timer()
print "Feature selection running time is: %f" % (t2-t1)

X = x0[:, fsub]
y = y0
print "%d features are selected" % X.shape[1]

## model training ========================================
t1= timeit.default_timer()
clf, ytrain, yscore = iForestTrain_hq(X,r=0.051)
#clf, ytrain, yscore = iForestTrain_hq(X[y==2,:])
t2 = timeit.default_timer()
print "Model training time is: %f" % (t2-t1)
plotHist(yscore)

## model predicting ========================================
t1= timeit.default_timer()
xtest = x1[:,fsub]
ytest, testScore = iForestPredict_hq(xtest, clf, ytrain, yscore)
t2 = timeit.default_timer()
print "Model predicting time is: %f" % (t2-t1)
#print [ytest.tolist().count(-1), ytest.tolist().count(1)]
#ytest #-1 negative; 1 positive


## model metrics ========================================
#testScore = (testScore - min(testScore)) / (max(testScore) - min(testScore))
plotHist(testScore)

from sklearn.metrics import classification_report
yt_ = ytest
yt_[ytest == 1] = 0
yt_[ytest == -1] = 1
print classification_report(y1, yt_)

auc = auc_hq(y1,testScore, pos_label=0)
accuracy = accuracy_hq(y1,yt_)
recall = recall_hq(y1,yt_)
precision = precision_hq(y1,yt_)
print "AUC value of model is: %f" % auc
print "Accuracy value of model is: %f" % accuracy
print "Recall value of model is: %f" % recall[0]
print "Precision value of model is: %f" % precision[0]


#=========================================================
auc, accuracy, recall, precision, sthr = allMetrics(y1, testScore, pos_label=0, average=None)
print "AUC value of model is: %f" % auc
print "Accuracy value of model is: %f" % accuracy
print "Recall value of model is: %f" % recall[0]
print "Precision value of model is: %f" % precision[0]

