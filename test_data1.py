# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 14:25:51 2017

@author: User327
"""

def test_data1():
    from sklearn.datasets import make_classification
    x, y = make_classification(n_samples =100000,
                           n_features = 200, 
                           n_informative = 50, 
                           n_redundant = 10, 
                           n_clusters_per_class = 2, 
                           flip_y = 0.001,
                           weights = [0.9,0.1],
                           class_sep = 3)
    x0 = x[:int(0.8*len(x))]
    y0 = y[:int(0.8*len(y))]
    x1 = x[int(0.8*len(x)):]
    y1= y[int(0.8*len(y)):]
    return(x0, y0, x1, y1)


def test_data2():
    import numpy as np
    ## 10000 customers
    customers = []
    for i in range(10000):
        n1 = ''
        for j in range(18):
            n1 = n1 + str(np.random.randint(0,9))
        customers.append(n1)
    
    ## 40 products
    products = []
    tmp = np.random.randint(2, size=160)
    for i in range(40):
        k=i*4
        n2 = ''
        for j in range(4):
            n2 = n2 + str(tmp[k+j])
        products.append(n2)
    
    ## 0 1 state, 100000 trades
    #states = [0]*90000 + [1]*10000
    states = np.random.randint(2, size=100000)
    
    ## 4 types
    typet = ['0101','0000','1111','0011']
    
    ## trades money
    np.random.seed(0)
    money = np.random.lognormal(5, 0.5, 100000)
    
    #打印表中的数据
    file_object = open('test_data2.csv', 'w')
    #https://www.zhihu.com/question/35455996
    #http://niewj.iteye.com/blog/1679100
    import datetime
    import time
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    a = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    fmat = "%Y-%m-%d %H:%M:%S"
    
    for i in range(100000):
        tmp1 = customers[np.random.randint(0,9999)]
        tmp1 = tmp1 + ',' + products[np.random.randint(0,39)]
        tmp1 = tmp1 + ',' + str(states[i])
        tmp1 = tmp1 + ',' + typet[np.random.randint(0,3)]
        tmp1 = tmp1 + ',' + str(money[i])
        a = strftime(strptime(a, fmat) + datetime.timedelta(0.003), fmat)
        tmp1 = tmp1 + ',' +  a.replace(' ', ',')
        file_object.write(tmp1.encode('utf-8') + '\n')
    file_object.close()

#test_data2()
    
    