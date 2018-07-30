# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:43:38 2017

@author: woon.zhenhao
"""

import keys
import time
import datetime
import apiconnector as ac
import json
import pandas as pd

urllist={
        'categories':'https://partner.shopeemobile.com/api/v1/item/categories/get',
        'attributes':'https://partner.shopeemobile.com/api/v1/item/attributes/get',
        'logistics':'https://partner.shopeemobile.com/api/v1/logistics/channel/get',
        "listing":"https://partner.shopeemobile.com/api/v1/item/add"
        }

server='live'
delim=';'
account='mcgraw'
d=datetime.datetime.now()
unixtime = int(time.mktime(d.timetuple()))

def getBody(account, query, itemid):
    global server
    
    shopID, PartnerID, Secret = keys.getDetails(account, server)
    print(shopID)
    print(PartnerID)
    
    body={
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime,
           "category_id": 11622,
           "name":"testwed",
           "description": "testusdfj sidhusd",
           "price":33.12,
           "stock": 1,
           "item_sku":"9780071452298",
#           "images":{
#                   "url":"data:image/jpeg;base64,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",
#                   },
#            "logistics":{
#                    "logistic_id":88011,
#                    "enabled": True
#                    },
            "weight": 0.1 
            }
    
    
    
#    if query == 'attributes':
#        body["category_id"]= itemid
        
    return body

def APIConnect(account, query, pid):
    url=urllist[query]
    body=getBody(account,query,pid)
    result, response = ac.getResponse(url, body, account, server)
    
    return result, response

df=APIConnect("mcgraw","listing", 1)

def addToList(optionsList, name, options):
    for i in optionsList:
        if name==i:
            ls=optionsList[i]
            ls=ls+options
            ls=list(set(ls))
            optionsList[name]=ls
            return optionsList
    
    optionsList[name]=options
    return optionsList

def getAttributes(account, query, pid, optionsList):
    url=urllist[query]
    body=getBody(account,query,pid)
    result, response = ac.getResponse(url, body, account, server)
    d=json.loads(response.content.decode('utf-8'))
    attrString=''
    result={}
    
    if len(d)==1:
        d=d['attributes']
        for i in d:
            name=i['attribute_name']
            options=i['options']
            optionsList=addToList(optionsList, name, options)
            
            attrString=attrString+delim+name
            optString=''
            for opt in options:
                optString=optString+opt+delim
            
            result[name]=optString
    
    return result, attrString, optionsList

def compileTables():
    result, response = APIConnect(account, 'categories','')
    d2=json.loads(response.content.decode('utf-8'))['categories']
    
    count=1
    attrCount=1
    attrAccumCount=1
        
    attrSets=pd.DataFrame(columns=['Category ID', 'Name', 'Has Child', 'Parent ID', 'Attributes'])
    optionSets=pd.DataFrame(columns=['Category ID', 'Name', 'Attribute Name', 'Options'])
    optionAccumSets=pd.DataFrame(columns=['Attribute Name', 'Values'])
    optionsList={}
    for i in d2:
        cat_id=i['category_id']
        cat_name=i['category_name']
        child=i['has_children']
        parent_id=i['parent_id']
        store=[cat_id, cat_name, child, parent_id]
        
        if child==False:
            result, attrString, optionsList=getAttributes(account,'attributes', cat_id, optionsList)
            for attrName in result:
                optionStore=[cat_id, cat_name]
                optionStore.append(attrName)
                optionStore.append(result[attrName])
                optionSets.loc[attrCount]=optionStore
                attrCount+=1
            store.append(attrString)
        else:
            store.append("")
        
        attrSets.loc[count]=store
        count+=1
        
    for name in optionsList:
        ls=[name]
        cur=optionsList[name]
        optstr=''
        for opt in cur:
            optstr=optstr+opt+delim
        
        ls.append(optstr)
        optionAccumSets.loc[attrAccumCount]=ls
        attrAccumCount+=1
        
    return attrSets, optionSets, optionAccumSets

#attrSets, optionSets, optionAccumSets=compileTables()
#
#attrSets.to_csv('categories.csv', header=True, index=False)   
#optionSets.to_csv('options.csv', header=True, index=False)    
#optionAccumSets.to_csv('optionsAccum.csv', header=True, index=False)
#    
    