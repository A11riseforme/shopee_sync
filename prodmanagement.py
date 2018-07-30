# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:13:51 2017

@author: woon.zhenhao
"""

import time
import datetime
import keys
import apiconnector as ac
import json
import pandas as pd
import os
import log
import math

d=datetime.datetime.now()
unixtime = int(time.mktime(d.timetuple()))
server=''


urllist={
     }

def getBody(account, query, itemid, stock, offset):
    
    shopID, PartnerID, Secret = keys.getDetails(account, server)
    
    body={
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime
            }
    
    if query == 'get products':
        body["pagination_offset"]=offset
        body["pagination_entries_per_page"]=100
    
    if query == 'product details':
        body["item_id"]= itemid
    
    if query == 'update stock':
        body["item_id"]= itemid
        body["stock"]= stock
        
    return body

def APIConnect(account, query, pid, stock, offset):
    url=urllist[query]
    body=getBody(account,query,pid, stock,offset)
    result, response = ac.getResponse(url, body, account, server)
    
    return result, response
    
def getProdList(account):    
    df=pd.DataFrame(columns=['item_id', 'SKU', 'name','description','stock', 'status'])
    success = False
    cont=True
    start=0
    
    while cont==True:
        result, response = APIConnect(account, 'get products','', '', start)
        
        if result == 'success':
            d2=json.loads(response.content.decode('utf-8'))
            d=d2['items']
            
            cont=d2['more']
            
            success = True
            
            for i in range(0,len(d)):
                tid=d[i]
                tid=tid['item_id']
                result, response2 = APIConnect(account, 'product details', tid,'','')
                d2=json.loads(response2.content.decode('utf-8'))
#                print(d2)
                pdata=d2['item']
                line=[tid,pdata['item_sku'],pdata['name'], pdata['description'],pdata['stock'], pdata['status']]
                df.loc[start+i]=line
                
            start+=100
        else:
            cont=False
            
    return success, df

def readInvenReport(account):
    found = False
    
    for f in os.listdir('./inventory report'):
        ind=str(f).find(str(account))
        if f[:1]!= '~' and ind > -1:
            name=f
            found = True
    
    if found==True:
#        xl=pd.ExcelFile('inventory report/'+name)
#        sheetnames = list(xl.sheet_names)
#        df=xl.parse(sheetnames[0])
        df=pd.read_csv('inventory report/'+name, encoding="ISO-8859-1")
        return True, df
    
    else:
        return False, None

def updateInven(account, itemid, sku, stock):
    result, response = APIConnect(account, 'update stock', int(itemid), int(stock),'')

    msg='Update '+str(itemid) +' / '+str(sku) +' to stock level: '+str(stock)+' for '+account+' - '+ result
    log.logMsg(msg)
    
    if result == 'fail':
        return False
    else:
        return True
    

def reconInven(si,ui, account):
    invenPercen=keys.getInvenPercen(account, server)
    
    updates = pd.DataFrame(columns=['item id','sku','description', 'shopee qty', 'urbanfox qty', 'updated qty'])
    
    success=0
    fail=0
    msg=''
    
    for i in range(len(si)):
        siQty=int(si.iloc[i,4])
        ssku=str(si.iloc[i,1])
        found=False
        
        for j in range(len(ui)):
            rawUiQty=int(ui.iloc[j,4])-int(ui.iloc[j,5])-int(ui.iloc[j,6])
            uiQty=math.ceil(max(rawUiQty,0)*invenPercen)
            usku=str(ui.iloc[j,0])
            if ssku.upper().strip()==usku.upper().strip():
                found=True
                if siQty!=uiQty:
                    if updateInven(account, si.iloc[i,0], si.iloc[i,1],uiQty):
                        updates.loc[success]=[si.iloc[i,0],si.iloc[i,1],si.iloc[i,2],siQty,rawUiQty,uiQty]
                        success+=1
                    else:
                        fail+=1
                break
            
        if found == False and siQty > 0:
            if updateInven(account, si.iloc[i,0], 0):
                success +=1
            else:
                fail+=1
    msg = str(success)+' successful updates, '+str(fail)+' failed updates. ' + 'Refer to log folder for more details'
    
    if success > 0:
        log.invenUpdatesCSV(updates, account)
    
    return msg

def updateUrbanInven(urbanInven, sku, qty):
    for j in range(len(urbanInven)):
        if str(urbanInven.iloc[j,0])==sku:
            urbanInven.iloc[j,4]=max(urbanInven.iloc[j,4]-qty,0)
            return urbanInven
        
    return urbanInven

def deductOrdFromInven(urbanInven, ordList):
    for i in ordList.index:
        row=ordList.loc[i]
        sku=row[1]
        qty=row[7]
        
        urbanInven=updateUrbanInven(urbanInven, sku, qty)
        
    return urbanInven
                
    
def main(account, serv, ordList,gotOrdList):
    global server
    server=serv
    
    global urllist
    if serv=='live':
        urllist={
                'get products': 'https://partner.shopeemobile.com/api/v1/items/get',
                'product details': 'https://partner.shopeemobile.com/api/v1/item/get',
                'update stock':'https://partner.shopeemobile.com/api/v1/items/update_stock'
                }
    else:
        urllist={
                'get products': 'https://partner.uat.shopeemobile.com/api/v1/items/get',
                'product details': 'https://partner.uat.shopeemobile.com/api/v1/item/get',
                'update stock':'https://partner.uat.shopeemobile.com/api/v1/items/update_stock'
         }
    
    shopeePass, shopeeInven=getProdList(account)
    
#    return shopeeInven
    
    msg=account+'-'
    
    if shopeePass:
        urbanPass, urbanInven = readInvenReport(account)
        
        if urbanPass:
            if gotOrdList:
                finalInven = deductOrdFromInven(urbanInven, ordList)
            else:
                finalInven = urbanInven
            msg=msg+reconInven(shopeeInven, finalInven, account)
            print(msg)
        else:
            msg=msg+'Failed to read inventory from urbanfox inventory folder'
            print(msg)
            
    else:
        msg=msg+'Failed to get product listing from shopee'
        print(msg)
        
    log.log('product', account, msg)
    
#    return shopeeInven, urbanInven, finalInven
