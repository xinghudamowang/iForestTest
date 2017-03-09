# -*- coding: utf-8 -*-

# http://scikit-learn.org/stable/auto_examples/ensemble/plot_isolation_forest.html

def iForestTrain_hq(X, r=0.1):
    import numpy as np
    from math import log
    from sklearn.ensemble import IsolationForest
    rng = np.random.RandomState(42)
    max_samples = min(int(X.shape[0]/2), max(int(log(X.shape[0]))+1, 512))
    clf = IsolationForest(max_samples=max_samples, random_state=rng, contamination=r)
    clf.fit(X)
    ytrain = clf.predict(X)
    yscore = clf.decision_function(X)
    return(clf, ytrain, yscore)

def iForestPredict_hq(X, clf, ytrain, yscore):
    ytest = clf.predict(X)
    testScore = clf.decision_function(X)
    return(ytest, testScore)  
