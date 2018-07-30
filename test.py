# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:41:51 2018

@author: woon.zhenhao
"""

import time
import datetime
import apiconnector as ac
import ordermanagement as om
import keys
import json


choices = ['mondelez','merries','kao', 'curel', 'books', 'kaocs', 'mcgraw']
account = choices[6]
server = 'live'

d=datetime.datetime.now()
unixtime = int(time.mktime(d.timetuple()))
unixtimeStart=int(time.mktime((d-datetime.timedelta(days=7)).timetuple()))

shopID, PartnerID, Secret = keys.getDetails(account, server)

url4='https://partner.shopeemobile.com/api/v1/orders/basics'
url='https://partner.uat.shopeemobile.com/api/v1/logistics/init_parameter/get'
url2='https://partner.uat.shopeemobile.com/api/v1/logistics/init'
url3 = 'https://partner.uat.shopeemobile.com/api/v1/logistics/channel/get'
url5 = 'https://partner.uat.shopeemobile.com/api/v1/item/categories/get'
url6 = 'https://partner.shopeemobile.com/api/v1/item/categories/get'
url7='https://partner.shopeemobile.com/api/v1/item/attributes/get'
url8="https://partner.shopeemobile.com/api/v1/item/add"

#body={
#           "shopid": shopID,
#           "partner_id": PartnerID,
#           "timestamp": unixtime,
#           "create_time_from": unixtimeStart,
#           "create_time_to": unixtime,
#           "pagination_entries_per_page": 50,
#           "pagination_offset": 0
#        }

order="180220103106APM"

body={
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime,
           "ordersn": order
        }

body2={
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime,
           "ordersn": order,
           "non_integrated":{
                   "tracking_no": "trc1234567890"
                   }
        }


def getBody(shopID, PartnerID, Secret):
    body={
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime,
           "create_time_from": unixtimeStart,
           "create_time_to": unixtime,
           "pagination_entries_per_page": 50,
           "pagination_offset": 0
            }
    
    return body

def getBody2(shopID, PartnerID, Secret, catId):
    global unixtime
    body={
           "category_id": catId,
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime
            }
    
    return body

body4={
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime,
           "create_time_from": unixtimeStart,
           "create_time_to": unixtime,
           "pagination_entries_per_page": 50,
           "pagination_offset": 0
       }

body3={
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime
        }

body5={
           "category_id": 4770,
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime
        }
         
success2, response2 = ac.getResponse(url7, body5, account,server)
#success2,response2 = ac.getResponse(url2, body2, account, server)
d=json.loads(response2.content)
cats=d['categories']
for cat in cats:
    cat_id = cat['category_id']
    parent = cat['parent_id']
    attrSuc, response = ac.getResponse(url6, getBody2(shopID, PartnerID, Secret, cat_id), account,server)
    d2 = json.loads(response.content)['attributes']
    
#    