# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:45:53 2017

@author: woon.zhenhao
"""

import time
from datetime import datetime
import prodmanagement as pm
import sys
import keys

start=time.time()

def checkAccuracy(choice):
    try:
        choice=int(choice)
    except ValueError:
        return False
    
    return True

#duration in seconds
def getChoice():
    cor=False
    
    while cor == False:
        choice=input('How many minutes would you like to schedule the program: ')
        cor=checkAccuracy(choice)
        
    return choice
    
def getAccountChoice():
    acc=keys.getAccounts()
    if len(acc)==0:
        print('Error in reading accounts. Please ensure file in folder account is correct.')
        return -1
    
    return acc

def runProcesses(acc):
    for i in acc:
        pm.main(str(i))
        
#acc=getAccountChoice()
#if acc!=-1:
#    dur = int(getChoice()) *60
#    print('Press ctrl + c to stop process')
#    start=time.time()
#        
#    try:
#        while True:
#            try:
#                print(datetime.now().strftime("%H:%M:%S"))
#                runProcesses(acc)
#                print('Press ctrl + c to stop process')
#                print()
#            except KeyboardInterrupt:
#                print("to be able to exit script gracefully while running")
#                sys.exit()
#            except Exception:
#                print("handle exceptions on a general level")
#            else:
#                time.sleep(dur)
#    
#    except KeyboardInterrupt:
#        print("to be able to exit script gracefully while sleeping")
#        sys.exit()