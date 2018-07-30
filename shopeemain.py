# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:08:30 2017

@author: woon.zhenhao
"""

import ordermanagement as om
import prodmanagement as pm
import keys
import codecs

action=['update product inventory','Retrieve orders', 'Update product inventory and retrieve orders']
server=['uat', 'live']

def checkAccuracy(choice, acc):
    try:
        choice=int(choice)
    except ValueError:
        return False
    
    if choice in range(0+1,len(acc)+1):
        return True
    else:
        return False

def getChoice(acc, query):
    cor=False
    choice=0
    
    while cor==False:
        for i in range(len(acc)):
            print(str(i+1)+') ' + acc[i])
            
        choice=input(query)
        cor=checkAccuracy(choice, acc)
        
        if cor==False:
            print('----Invalid Input. Please try again.----')
            print()
            
    return acc[int(choice)-1]

def getAccountChoice(server):
    acc=keys.getAccounts(server)
    if len(acc)==0:
        print('Error in reading accounts. Please ensure file in folder account is correct.')
        return -1
    
    return getChoice(acc,'Please choose account: ')

def getAction():
    
    return getChoice(action, 'Please choose action: ')

def getServerChoice():
    return getChoice(server, 'Please choose server: ')
    
def main():
    server=getServerChoice()
    acc = getAccountChoice(server)
    actionv = getAction()
    
    print(actionv)
    
    if actionv == action[0]:
        pm.main(str(acc), server,'', False)
        
    if actionv == action[1]:
        ordList=om.main(str(acc), server)
    
    if actionv == action[2]:
        ordList=om.main(str(acc), server)
        pm.main(str(acc), server, ordList, True)
        
while True:
    print('press ctrl+c to end process')
    main()
    print()
