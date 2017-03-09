o# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 15:54:40 2017

@author: User327
"""

### get features for no-recording customers

### outside functions
from test_data1 import *
from featureSelect1 import *
from isolation_score import *
from metrics_classifer import *

### inside tool functions
import numpy as np
def test1():
    ## data prepare ========================================
	
    ## customer filter ========================================

	## step 1: get cusotmer list 
    #oneCus = getOneList(customers, products, prods[i])
    ## step 2: get other feature from other tables, by sql fron database
    #newfea = getNewfeature(oneCus)
    ## step 3: get feature matrix
    #feaM = getCustomerVec(customers, products, oneCus, transM, p1, prodsList, prods, nbuy)
    ## step 4: get potential customer lists
    #testCus1 = getPotentialCus(customers, oneCus)
    #feaTest = getCustomerVec(customers, products, testCus1, transM, p1, prodsList, prods, nbuy)

    ## feature selection ========================================
    fsub = linearCoe_hq(x0, y0)
    X = x0[:, fsub]

    ## model training ========================================
    clf, ytrain, yscore = iForestTrain_hq(X,r=0.1)

    ## model predicting ========================================
    xtest = x1[:,fsub]
    ytest, testScore = iForestPredict_hq(xtest, clf, ytrain, yscore)
	
	s1 = np.array([0]*len(testScore))
	ntrain = len(ytrain)
	for i in range(len(testScore)):
		tmp = yscore <= testScore[i]
		s1[i] = tmp.count(True)/ntrain
    ## model metrics ========================================
    yt_ = ytest
    yt_[ytest == 1] = 0
    yt_[ytest == -1] = 1

    return(yt_,s1)

