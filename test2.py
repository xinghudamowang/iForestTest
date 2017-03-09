# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 09:13:55 2017

@author: User327
"""

## get data=====================================
from isolation_score import *
from metrics_classifer import *
from transMatrix import *
import numpy as np
import timeit 

customers, products, money = readFile('test_data2.csv')
testCus = customers[8500:10000]
testProd = products[8500:10000]

customers = customers[0:8500]
products = products[0:8500]

t1= timeit.default_timer()
prods = set(products)
prods = list(prods)     
transM, prodsList, p1 = getTransMatrix(customers, products, prods)
t2 = timeit.default_timer()
print "transform matrix escaping time is: %f" % (t2-t1) 

t1= timeit.default_timer()    
cusList, uniCus = customerList(customers, products)
t2 = timeit.default_timer()
print "customer list escaping time is: %f" % (t2-t1) 
 
custestList, unitestCus = customerList(testCus, testProd)

#nbuy = 0
#for i in range(len(prodsList)):
#    nbuy = nbuy + len(prodsList[i])
nbuy = len(set(customers))

## for each products, to run modeling process=================================
RecommendList = []
#for i in range(len(prods)):
for i in range(4,5):
    t1= timeit.default_timer()
    print "For product: %s" % prods[i]
    ## step 1: get cusotmer list 
    oneCus = getOneList(customers, products, prods[i])
    ## step 2: get other feature from other tables, by sql fron database
    newfea = getNewfeature(oneCus)
    ## step 3: get feature matrix
    feaM = getCustomerVec(uniCus, cusList, oneCus, transM, p1, prodsList, prods, nbuy)
    print "the size of training is: %d" % feaM.shape[0]
    ## step 4: get potential customer lists
    testCus1 = getPotentialCus(customers, oneCus)
    feaTest = getCustomerVec(uniCus, cusList, testCus1, transM, p1, prodsList, prods, nbuy)
    print "the size of testing is: %d" % feaTest.shape[0]
    ## step 5: train and predict model
    clf, ytrain, yscore = iForestTrain_hq(feaM,r=0.1)
    ytest, testScore = iForestPredict_hq(feaTest, clf, ytrain, yscore)
    yt_ = ytest
    yt_[ytest == 1] = 0
    yt_[ytest == -1] = 1
    ## step 6: get all metrics
    y1 = np.array([1] * len(ytest))
    for j in range(len(testCus1)):
        if testCus1[j] in testCus:
            tmp = custestList[unitestCus.index(testCus1[j])]
            if prods[i] in tmp:
                y1[j] = 0
    #print [y1.tolist().count(0), y1.tolist().count(1)]
    
           
    auc, accuracy, recall, precision, sthr = allMetrics(y1, testScore, pos_label=0, average=None)
    print "AUC value of model is: %f" % auc
    print "Accuracy value of model is: %f" % accuracy
    print "Recall value of model is: %f" % recall[0]
    print "Precision value of model is: %f" % precision[0]
    ##step 7: get recommend lists
    onelist = sorted(zip(map(lambda x: round(x, 4), testScore), testCus1))
    print onelist[0]
    ##onelist = [testCus1[ii] for ii, x in enumerate(yt_) if x==0]
    #RecommendList.append(onelist)
    t2 = timeit.default_timer()
    print "Escaping time is: %f" % (t2-t1) 



