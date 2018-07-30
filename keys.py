# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:06:40 2017

@author: woon.zhenhao
"""

import os
import pandas as pd

def readReport(server):
    found = False
    
    if server=='live':
        folderName = 'account'
    else:
        folderName = 'account(uat)'
    
    for f in os.listdir('./'+folderName):
        if f[:1]!= '~':
            name=f
            found = True
    
    if found==True:
        df=pd.read_csv(folderName+'/'+name)
        return True, df
    
    else:
        return False, None
    
def getInvenPercen(account, server):
    res,df=readReport(server)
    
    for i in df.index:
        row=df.loc[i]
        
        if row['Account']== account:
            return row['inventory percentage']
    
    return ''

#t=getInvenPercen('mondelez', 'live')

def getAccounts(server):
    res, df=readReport(server)
    return list(df['Account'])

def getDetails(account, server):
    res, df=readReport(server)
    for i in range(len(df)):
        if str(df.iloc[i,0]) == str(account):
            return int(df.iloc[i,1]),int(df.iloc[i,2]),df.iloc[i,3]
        
    return '','',''