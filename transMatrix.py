# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 10:16:58 2017

@author: User327
"""

### get probability transform matrix from table

def readFile(filename, cols=None):
    fileOb = open(filename,'r')
    customers = []
    products = []
    money = []
    for line in fileOb:
        segline = line.split(',')
        customers.append(segline[0])
        products.append(segline[1])
        money.append(float(segline[4]))
    fileOb.close()
    return(customers, products, money)

def getOneList(customers, products, prod):
    ## get customer lists
    cus = [customers[ii] for ii, x in enumerate(products) if x == prod]
    cus = set(cus)
    cus = list(cus)
    return(cus)
    
def getNewfeature(custs):
    return(custs)
    
def getTransMatrix(customers, products, prods):
    ## get trans matrix
    import numpy as np
    n_prod = len(prods)
    
    #step 1: estimate one to itself=========================
    pairs = []
    for i in range(len(products)):
        tmp1 = customers[i] + '_' + products[i]
        pairs.append(tmp1)
    
    uniPair = set(pairs)
    """
    #pii = (len(pairs) - len(uniPair))/len(pairs)
    kii = 0
    for item in uniPair:
        tmp1 = pairs.count(item)
        if tmp1 > 2:
            kii = kii+tmp1-2
    pii = kii/len(pairs)
    """
    pii = np.array([0]*n_prod)
    for i in range(n_prod):
        tmpair = [pairs[ii] for ii, x in enumerate(products) if x == prods[i]]
        oneuni = set(tmpair)
        kii = 0
        for item in oneuni:
            tmp = tmpair.count(item)
            if tmp > 2:
                kii = kii + tmp - 2
        pii[i] = kii/len(tmpair)
    
    #step 2: estimate i to j========================
    cus1 = []
    prod1 = []
    for item in uniPair:
        tmp1= item.split('_')
        cus1.append(tmp1[0])
        prod1.append(tmp1[1])
    
    """
    kij0 = 0   
    uniCus1 = set(cus1)
    for item in uniCus1:
        tmp1 = cus1.count(item)
        if tmp1 >= 2:
            kij0 = kij0+1
    pij0 = kij0/len(uniCus1)
    """
    
    kij0 = 0
    k1 = 0
    ncus1 = len(cus1)
    uniCus1 = set(cus1)
    for item in uniCus1:
        tmp1 = cus1.count(item)
        kij0 = kij0+tmp1-1
        if tmp1==1:
            k1 = k1+1
    pij0 = kij0/ncus1
    p1 = k1/len(uniCus1)
    
    prodsList = []
    numii = np.array([0]*n_prod)
    for i in range(n_prod):
        tmp1 = [cus1[ii] for ii, x in enumerate(prod1) if x == prods[i]]
        numii[i] = len(tmp1)
        prodsList.append(tmp1)
    
    transM = 1.0*np.arange(n_prod*n_prod).reshape(n_prod, n_prod)    
    for i in range(n_prod):
        for j in range(n_prod):
            if i==j:
                transM[i,j] = pii[i]
            else:
                tmp1 = list(set(prodsList[i]).intersection(set(prodsList[j])))
                transM[i,j] = len(tmp1)/numii[i]
            if transM[i,j] == 0:
                transM[i,j] = pij0 * numii[j]/ncus1
    
    return(transM, prodsList, p1)

def customerList(customers, products):
    uniCus = set(customers)
    uniCus = list(uniCus)
    cusList = []
    for item in uniCus:
        tmp = [products[ii] for ii, x in enumerate(customers) if x == item]
        tmp = list(set(tmp))
        cusList.append(tmp)
    return(cusList, uniCus)
    
def getCustomerVec(uniCus, cusList, cusSet, transM, p1, prodsList, prods, nbuy):
    import numpy as np
    ## get all feature vectors   
    n_prod = len(prods)
    n_cus = len(cusSet)
    X = 1.0*np.arange(n_prod*n_cus).reshape(n_cus, n_prod)
    for i in range(n_cus):
        for j in range(n_prod):
            if cusSet[i] in prodsList[j]:
                X[i,j] = 1.0
            else:
                tmprod = cusList[uniCus.index(cusSet[i])]
                if len(tmprod)==1:
                    X[i,j] = transM[prods.index(tmprod[0]),j]
                elif len(tmprod)==2:
                    X[i,j] = max(transM[prods.index(tmprod[0]),j], transM[prods.index(tmprod[1]),j])/2
                elif len(tmprod)>=3:
                    X[i,j] = (1.0/(2**len(tmprod))) * (len(prodsList[j])/nbuy)
                    
    return(X)

def getPotentialCus(customers, oneCus):
    allCus = set(customers)
    testCus = allCus.difference(set(oneCus))
    testCus = list(testCus)
    return(testCus)
