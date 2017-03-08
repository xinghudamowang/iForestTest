# -*- coding: utf-8 -*-

import numpy as np

def pearsonr_hq(X, y, cut=0.05):
    from scipy.stats import pearsonr
    nf = X.shape[1]
    subs = np.array([False] * nf)
    for i in range(nf):
        subs[i] = (pearsonr(X[:,i], y)[1] < cut)
    return(subs)
    

def mic_hq(X, y, cut=0.2):
    from minepy import MINE
    m = MINE()
    nf = X.shape[1]
    subs = np.array([False] * nf)
    for i in range(nf):
        m.compute_score(X[:,i], y)
        subs[i] = (m.mic() < cut)
    return(subs)
     

def RFcross_hq(X, y):
    ### RF cross validation =====================
    from sklearn.cross_validation import cross_val_score, ShuffleSplit
    from sklearn.ensemble import RandomForestRegressor
    from math import log
    n_estimators = max(int(log(X.shape[0]))+1, 100)
    max_depth = max(int(log(X.shape[1]))+1, 5)
    rf = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth)
    scores = []
    for i in range(X.shape[1]):
        score = cross_val_score(rf, X[:, i:i+1], y, scoring="r2",
                              cv=ShuffleSplit(len(X), 3, .3))
        #scores.append((round(np.mean(score), 3), names[i]))
        scores.append(round(np.mean(score), 3))
    return scores


def linearCoe_hq(X, y, cut=0.05):
    ## linear model coefficient based=====
    from sklearn.feature_selection import f_regression
    f, pval  = f_regression(X, y, center=True)
    subs = np.array([False] * X.shape[1])
    subs[pval < cut] = True
    return(subs)


def lasso_hq(X, y, alpha=0.3):
    ## feature select based on Lasso=====
    from sklearn.linear_model import RandomizedLasso
    rlasso = RandomizedLasso(alpha=alpha)
    rlasso.fit(X, y)
    return(rlasso.scores_)

    
def Ridge_hq(X, y, alpha=2):
    ### feature select based on Ridge=====
    from sklearn.linear_model import Ridge
    ridge = Ridge(alpha=alpha)
    ridge.fit(X,y)
    return(ridge.coef_)
	
    
def RFgini_hq(X, y):
    ## RF gini importance ===
    from sklearn.ensemble import RandomForestRegressor
    rf = RandomForestRegressor()
    rf.fit(X, y)
    return(rf.feature_importances_)


def rfShuffle_hq(X, Y):
    ## shuffle orders of one feature===
    from sklearn.cross_validation import ShuffleSplit
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score
    rf = RandomForestRegressor()
    scores = []
    for train_idx, test_idx in ShuffleSplit(len(X), 100, .3):
        X_train, X_test = X[train_idx], X[test_idx]
        Y_train, Y_test = Y[train_idx], Y[test_idx]
        rf.fit(X_train, Y_train)
        acc = r2_score(Y_test, rf.predict(X_test))
        for i in range(X.shape[1]):
            X_t = X_test.copy()
            np.random.shuffle(X_t[:, i])
            shuff_acc = r2_score(Y_test, rf.predict(X_t))
            scores.append((acc-shuff_acc)/acc)
    return(scores)

    
def randomLasso_hq(X, y, alpha=0.025):
    ### random lasso or logistic regression =======
    from sklearn.linear_model import RandomizedLasso
    rlasso = RandomizedLasso(alpha=alpha)
    rlasso.fit(X, y)
    return(rlasso.scores_)

    
def RFE_hq(X, y):
    ### RFE method====
    from sklearn.feature_selection import RFE
    from sklearn.linear_model import LinearRegression
    #use linear regression as the model
    lr = LinearRegression()
    #rank all features, i.e continue the elimination until the last one
    rfe = RFE(lr, n_features_to_select=1)
    rfe.fit(X,y)
    return(rfe.ranking_)


def testFeatureSelect1():
    ## test ======
    import timeit
    from sklearn.datasets import load_boston
    boston = load_boston()
    X = boston["data"]
    y = boston["target"]

    t1= timeit.default_timer()
    a1 = pearsonr_hq(X,y)
    t2 = timeit.default_timer()
    print t2-t1
    
    t1= timeit.default_timer()
    a2 = mic_hq(X,y)
    t2 = timeit.default_timer()
    print t2-t1
    
    t1= timeit.default_timer()
    a3 = RFcross_hq(X, y)
    t2 = timeit.default_timer()
    print t2-t1
    
    t1= timeit.default_timer()
    a4 = linearCoe_hq(X, y)
    t2 = timeit.default_timer()
    print t2-t1
    
    t1= timeit.default_timer()
    a5 = lasso_hq(X, y)
    t2 = timeit.default_timer()
    print t2-t1
    
    t1= timeit.default_timer()
    a6 = Ridge_hq(X, y)
    t2 = timeit.default_timer()
    print t2-t1
    
    t1= timeit.default_timer()
    a7 = RFgini_hq(X, y)
    t2 = timeit.default_timer()
    print t2-t1
    
    t1= timeit.default_timer()
    a8 = rfShuffle_hq(X, y)
    t2 = timeit.default_timer()
    print t2-t1
    
    t1= timeit.default_timer()
    a9 = randomLasso_hq(X, y)
    t2 = timeit.default_timer()
    print t2-t1
    
    t1= timeit.default_timer()
    a10 = RFE_hq(X, y)
    t2 = timeit.default_timer()
    print t2-t1
    
    
