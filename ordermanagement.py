# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:04:27 2017

@author: woon.zhenhao
"""

import time
import datetime
import keys
import apiconnector as ac
import log
import json
import pandas as pd
import masterReader as mr

d=datetime.datetime.now()
unixtime = int(time.mktime(d.timetuple()))

server=''

unixtimeStart=int(time.mktime((d-datetime.timedelta(days=7)).timetuple()))

urllist={
     }

df=''

def getOrders(account, ordCount):
#    ordCount=0
    passOrdCount=0
    result, response = APIConnect(account, 'get orders',ordCount,'')
    
    if result == 'success':
        df=json.loads(response.content.decode('utf-8'))
        more=df['more']
        cont=more
        print(cont)
        orders=df['orders']
        
        ordList=[]
        
        for i in orders:
            status=i['order_status']
            SO = i['ordersn']
            
            msg=str(SO)+'-'+str(status)
            log.logMsg(msg)
            
            if status == 'READY_TO_SHIP':
                ordList.append(str(SO))
                passOrdCount+=1
                
            ordCount+=1
    
        return True, ordCount, passOrdCount, cont, ordList
    
    return False, '','',False,''
    

def getOrderDets(account, ordList):
    rowCount=0
    
    orderList=pd.DataFrame(columns=['SO', 'SKU', 'Payment', 'name','address','postal','phone', 'qty', 'unitPrice', 'TotPrice', 'Remarks', 'status'])
    result, response = APIConnect(account, 'get order details', '',ordList)
    df2=json.loads(response.content.decode('utf-8'))
    ordDets=df2['orders']
    
    for i in ordDets:
        SO = i['ordersn']
        payment='Paid'
        BDets=i['recipient_address']
        name=BDets['name']
        address=BDets['full_address']
        postal=BDets['zipcode']
        phone=BDets['phone']
        totP=i['total_amount']
        remarks=i['message_to_seller']
        ordStatus=i['order_status']
        
        for j in i['items']:
            SKU = j['item_sku']
            qty=j['variation_quantity_purchased']
            unitP=j['variation_discounted_price']
            lst=[SO,SKU,payment, name, address, postal, phone, qty,unitP, totP, remarks, ordStatus]
            
            orderList.loc[rowCount]=lst
            rowCount+=1
            
    return orderList,rowCount

# pulls only orders which are ready to ship
def getOrderList(account):
    cont=True
    rowCount=0
    ordCount=0
    passOrdCount=0
    
    log.logMsg('')
    log.logMsg('All orders retrieved')
    
    masterOrderList=pd.DataFrame(columns=['SO', 'SKU', 'Payment', 'name','address','postal','phone', 'qty', 'unitPrice', 'TotPrice', 'Remarks', 'status'])
    
    while cont:
        result, ordCount2, passOrdCount2, cont, ordList = getOrders(account, ordCount)
        if result==True:
            ordCount+=ordCount2
            passOrdCount+=passOrdCount2
            
            if len(ordList)>0:
                orderList, rowCount = getOrderDets(account, ordList)
                masterOrderList=masterOrderList.append(orderList)
    
    if result==True:
        msg= str(ordCount)+' orders retrieved, '+str(passOrdCount)+' orders under READY_TO_SHIP,'
        return True,masterOrderList, msg
    else:
        msg= 'Cannot connect to shopee'
        return False, '', msg

def getBody(account, query, offset, ordList):
    
    shopID, PartnerID, Secret = keys.getDetails(account, server)
    
    if query == 'get orders':
        body={
               "shopid": shopID,
               "partner_id": PartnerID,
               "timestamp": unixtime,
               "create_time_from": unixtimeStart,
               "create_time_to": unixtime,
               "pagination_entries_per_page": 50,
               "pagination_offset": offset
                }
    
    if query == 'get order details':
        body={
               "shopid": shopID,
               "partner_id": PartnerID,
               "timestamp": unixtime,
               "ordersn_list": ordList
                }
        
    return body

def APIConnect(account, query, offset, ordList):
    url=urllist[query]
    body=getBody(account,query, offset, ordList)

    result, response = ac.getResponse(url, body, account, server)
    
    return result, response

def found(a,ls):
    for i in ls:
        if str(a)==str(i):
            return True
        
    return False 

def reconOrders(so,uo,account):
    mList=pd.DataFrame(columns=['SO','tot','date','account'])
    upList=pd.DataFrame(columns=['SO', 'SKU', 'Payment', 'name','address','postal','phone', 'qty', 'unitPrice', 'TotPrice', 'Remarks', 'status'])
    urow=0
    mrow=0
    prev=''
    msg=''
    
    log.logMsg('')
    log.logMsg('New orders')
    log.logMsg('[SO, SKU, Payment, name, address, postal, phone, qty, unitPrice, TotPrice, Remarks, status]')
    
    for i in so.index:
        ls=so.loc[i]
        sid=ls[0]
        tot=ls[9]
        status=ls[11]

        if found(sid,uo)==False:
            
            if sid!=prev:
                log.logMsg(str(sid)+'-'+str(status))
                mList.loc[mrow]=[sid,tot, d.strftime("%d-%m-%y_%H:%M:%S"), account]
                mrow+=1
                prev=sid
                
            log.logMsg(str(list(ls)))
            upList.loc[urow]=ls
            urow+=1
            
    msg+= str(mrow)+' new orders and recorded in template, ' + str(urow)+' new order lines recorded in template. '
    
    mr.writeToMaster(mList)
    mr.writeToTemplate(upList, account)
    
    return msg, upList

def main(account, serv):
    ordList=pd.DataFrame(columns=['SO', 'SKU', 'Payment', 'name','address','postal','phone', 'qty', 'unitPrice', 'TotPrice', 'Remarks', 'status'])
    global server
    server=serv
    global urllist
    if serv == 'live':
        urllist={
             'get orders': 'https://partner.shopeemobile.com/api/v1/orders/basics',
             'get order details':'https://partner.shopeemobile.com/api/v1/orders/detail'
             }
    else:
        urllist={
             'get orders': 'https://partner.uat.shopeemobile.com/api/v1/orders/basics',
             'get order details':'https://partner.uat.shopeemobile.com/api/v1/orders/detail'
             }
    
    
    msg=str(account)+'-'
    shopeePass, shopeeOrders, msg1 = getOrderList(account)
    
    if shopeePass:
        if len(shopeeOrders)==0:
            msg+='No ready to ship orders from shopee - '
            print(msg)
        else:
            urbanPass, urbanOrders = mr.getOrdList()
#       
            if urbanPass:
                msg2, ordList=reconOrders(shopeeOrders, urbanOrders, account)
                msg+=msg1+ msg2+'Refer to log file for more details.'
                print(msg)
            else:
                msg+='Failed to read historical orders'
                print(msg)
            
    else:
        msg+='Failed to get order listing from shopee'
        print(msg)
        
    log.log('orders', account, msg)
    
    return ordList
     