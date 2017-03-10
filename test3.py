# -*- coding: utf-8 -*-

### the simple version for existing customers

def getTransMatrix0(customers, products):
    ## get trans matrix 
    prods = set(products)
    prods = list(prods)
    prodsList = []
    for item in prods:
        tmp = [customers[ii] for ii, x in enumerate(products) if x == item]
        tmp = list(set(tmp))
        prodsList.append(tmp)
    
    """
    prods = []
    n_prod = len(set(products))
    prodsList = [None] * n_prod
    for i in range(len(customers)):
        if products[i] not in prods:
            prods.append(products[i])
        if (prodsList[prods.index(products[i])]==None):
            prodsList[prods.index(products[i])] = customers[i]
        else:
            prodsList[prods.index(products[i])] = prodsList[prods.index(products[i])] + customers[i]
    """
    
    n_prod = len(prods)
    transM = 1.0*np.arange(n_prod*n_prod).reshape(n_prod, n_prod)    
    for i in range(n_prod):
        for j in range(n_prod):
            tmp1 = len(set(prodsList[i]).intersection(set(prodsList[j])))
            tmp2 = len(set(prodsList[i]).union(set(prodsList[j])))
            transM[i,j] = 1.0*tmp1/tmp2
            
            
    return(transM, prodsList, prods)


def getCustomerVec0(transM, customers, products, prods, prodsList, cusList, unicus, alpha=0.99):
    import numpy as np
    ## get all feature vectors   
    n_prod = len(prods)
    n_cus = len(unicus)
    numii = np.array([0.0]*n_cus)
    for i in range(n_cus):
        numii[i] = customers.count(unicus[i])
        
    X = 1.0*np.arange(n_prod*n_cus).reshape(n_cus, n_prod)
    for i in range(n_cus):
        for j in range(n_prod):
            if unicus[i] in prodsList[j]:
                X[i,j] = alpha * prodsList[j].count(unicus[i])/numii[i]
            else:
                #item = cusList[i][0]
                #X[i,j] = alpha*(prodsList[prods.index(item)].count(unicus[i])/numii[i] )*transM[prods.index(item),j]
                X[i,j] = 0
                for item in set(cusList[i]):
                    X[i,j] = X[i,j] + alpha*(prodsList[prods.index(item)].count(unicus[i])/numii[i] )*transM[prods.index(item),j]

            if X[i,j] == 0:
                X[i,j] = np.random.uniform(0,1.0-alpha)
                    
    return(X)

    
def recommendList(X, unicus, prods):
    rdList = []
    for i in range(len(prods)):
        onelist = sorted(zip(unicus, map(lambda x: round(x, 10), -1*X[:,i])))
        rdList.append(onelist)
    return(rdList)

def customerList0(customers, products):
    ncus = len(set(customers))
    cusList = [None] * ncus
    unicus = []
    for i in range(len(customers)):
        if customers[i] not in unicus:
            unicus.append(customers[i])
        if (cusList[unicus.index(customers[i])]==None):
            cusList[unicus.index(customers[i])] = [products[i]]
        else:
            cusList[unicus.index(customers[i])].append(products[i])
    return(cusList, unicus)  

def filterRdList(rdList, dutime, customers, products, dates, unicus, prods):
    import datetime
    import numpy as np
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    fmat = "%Y-%m-%d"
    customers = np.array(customers)
    products = np.array(products)
    #dates = np.array(dates)
    targeT = '2017-10-01'
    
    dropList = [None] * len(rdList)
    
    for i in range(len(rdList)):
        for j in range(len(rdList[i])):
            cus1 = rdList[i][j][0]
            ind1 = np.where(customers==cus1)
            ind2 = np.where(products==prods[i])
            inInd = np.intersect1d(ind1,ind2)
            if len(inInd)>0:
                amax = max(inInd)
                endtime = strftime(strptime(dates[amax], fmat) + datetime.timedelta(dutime[i]), fmat)
                if strptime(endtime, fmat) > strptime(targeT,fmat):
                    if (dropList[i]==None):
                        dropList[i] = [j]
                    else:
                        dropList[i].append(j)
    
    rdList1 = rdList
    for k in range(len(rdList)):
        if not (dropList[k]==None):
            rdList1[k] = [i for j, i in enumerate(rdList[k]) if j not in dropList[k]]
        
    return(rdList1)   
    
### test section ==============================================================
from metrics_classifer import *
from transMatrix import *
import numpy as np
import timeit 

customers, products, money, dates = readFile('test_data2.csv')
customers = customers[:5000]
products = products[:5000]
dates = dates[:5000]

t1 = timeit.default_timer()
transM, prodsList, prods = getTransMatrix0(customers, products)
t2 = timeit.default_timer()
cusList, unicus = customerList0(customers, products)
#cusList, unicus = customerList(customers, products)
t3 = timeit.default_timer()
X = getCustomerVec0(transM, customers, products, prods, prodsList, cusList, unicus, alpha=0.9)
print X.shape
t4 = timeit.default_timer()
rdList = recommendList(X, unicus, prods)
t5 = timeit.default_timer()
print "Escaping time is: %f" % (t2-t1) 
print "Escaping time is: %f" % (t3-t2) 
print "Escaping time is: %f" % (t4-t3) 
print "Escaping time is: %f" % (t5-t4) 

#print rdList[0][1][0] 

## filter by 产品有效截止日
import random
n_prod = len(prods)
dutime = [ii*40 for ii in range(1,n_prod+1)]
random.shuffle(dutime)
t5 = timeit.default_timer()
rdList1 = filterRdList(rdList, dutime, customers, products, dates, unicus, prods)
## filters by only buying !!!!!!
t6 = timeit.default_timer()
print "drop buying Escaping time is: %f" % (t6-t5) 

