# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:35:33 2017

@author: User327
"""
import timeit
import cx_Oracle 
import pandas as pd

conn = cx_Oracle.connect('bank/bank@172.16.2.248/orcl') 
cur = conn.cursor() 

## get all customer ids =======================================================
"""
cur.execute('select ECIF_NUM FROM CUSTOMER_F_20161230')
t1 = timeit.default_timer()
numR = 10000
customers = []
for i in range(numR):
    x = cur.fetchone()
    customers.append(str(x[0]))
    
t2 = timeit.default_timer()
print "Escaping time is: %f" % (t2-t1) 
"""

## get trading customers and time pairs =======================================
#cur.execute("select ECIF_NUM, TX_DT from ev_tx_flow_event_rfs where RMB_CHREM_TX_CD = '1266'")
#cur.execute("select ECIF_NUM, TX_DT from ev_tx_flow_event_rfs where RMB_CHREM_TX_CD in ('1266','1267','1268')")
#cur.execute("select * from EV_TX_FLOW_EVENT_RFS where RMB_CHREM_TX_CD like '12__' ")
cur.execute("select * from EV_TX_FLOW_EVENT_RFS")
x0 = cur.fetchall()
cols0 = [des[0] for des in cur.description]
tab0 = pd.DataFrame(x0, columns=cols0)

"""
t1 = timeit.default_timer()
pairs = []
for i in range(len(x)):
    pairs.append([x[i][0],x[i][1]])   
t2 = timeit.default_timer()
print "Escaping time is: %f" % (t2-t1) 
"""

### get all features from different tables ====================================
"""
cur.execute("select table_name FROM user_tables")
x = cur.fetchall()
print x
"""

#!!! cur.execute("select column_name FROM information_schema.COLUMNS where table_name = 'EV_TX_FLOW_EVENT_RFS' ")


# get from CM_AG_DEBIT_CARD_BAL_SUM_D
t1 = timeit.default_timer()
#cur.execute("select * from (select ECIF_NUM, TX_DT from EV_TX_FLOW_EVENT_RFS where RMB_CHREM_TX_CD like '12__') A, CM_AG_DEBIT_CARD_BAL_SUM_D B, where A.ECIF_NUM=B.CUST_NUM and A.TX_DT=B.STAT_DT")
cur.execute("select * from (select ECIF_NUM, TX_DT from EV_TX_FLOW_EVENT_RFS) A, CM_AG_DEBIT_CARD_BAL_SUM_D B where A.ECIF_NUM=B.CUST_NUM and A.TX_DT=B.STAT_DT")
x1 = cur.fetchall()
cols1 = [des[0] for des in cur.description]
tab1 = pd.DataFrame(x1, columns=cols1)
t2 = timeit.default_timer()
print "Escaping time is: %f" % (t2-t1) 


# get from CM_PT_CRM_LKMAN_OPEN_IND_D
t1 = timeit.default_timer()
cur.execute("select * from (select ECIF_NUM, TX_DT from EV_TX_FLOW_EVENT_RFS) A, CM_PT_CRM_LKMAN_OPEN_IND_D B where A.ECIF_NUM=B.CUST_NUM_ECIF and A.TX_DT=B.STAT_DT")
x2 = cur.fetchall()
cols2 = [des[0] for des in cur.description]
tab2 = pd.DataFrame(x2, columns=cols2)
t2 = timeit.default_timer()
print "Escaping time is: %f" % (t2-t1) 


# get from CM_PT_CRM_CUST_AUM_D
t1 = timeit.default_timer()
cur.execute("select * from (select ECIF_NUM, TX_DT from EV_TX_FLOW_EVENT_RFS) A, CM_PT_CRM_CUST_AUM_D B where A.ECIF_NUM=B.CUST_NUM_ECIF and A.TX_DT=B.STAT_DT")
x3 = cur.fetchall()
cols3 = [des[0] for des in cur.description]
tab3 = pd.DataFrame(x3, columns=cols3)
t2 = timeit.default_timer()
print "Escaping time is: %f" % (t2-t1) 

cur.close()
#conn.commit()
conn.close()


### write to tables
tab01 = pd.merge(tab0, tab1, how='left', on=['ECIF_NUM', 'TX_DT'])
tab012 = pd.merge(tab01, tab2, how='left', on=['ECIF_NUM', 'TX_DT'])
tab0123 = pd.merge(tab012, tab3, how='left', on=['ECIF_NUM', 'TX_DT'])
tab0123.to_csv('test1orcl.csv', sep=',', index=False, header=True)

