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

account = 'mondelez'
server = 'uat'

d=datetime.datetime.now()
unixtime = int(time.mktime(d.timetuple()))
unixtimeStart=int(time.mktime((d-datetime.timedelta(days=7)).timetuple()))

shopID, PartnerID, Secret = keys.getDetails(account, server)

#url='https://partner.uat.shopeemobile.com/api/v1/orders/basics'
url='https://partner.uat.shopeemobile.com/api/v1/logistics/init_parameter/get'
url2='https://partner.uat.shopeemobile.com/api/v1/logistics/init'
url3 = 'https://partner.uat.shopeemobile.com/api/v1/logistics/channel/get'

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

body3={
           "shopid": shopID,
           "partner_id": PartnerID,
           "timestamp": unixtime
        }
         
#success2, response2 = ac.getResponse(url, body, account,server)
success2,response2 = ac.getResponse(url2, body2, account, server)
d=json.loads(response2.content)

print(response2.content)