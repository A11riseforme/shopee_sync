# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:57:36 2017

@author: woon.zhenhao
"""

import requests
import json
from hashlib import sha256
from hmac import HMAC
import keys

def APIConnect(url,header, body):
    response=requests.post(url,data=body, headers=header)                               
    
    if (response.status_code)==200:
        return 'success', response
    else:
        print(response.content)
        return 'fail', response
    
def getFields(url, body, account, server):
    
    shopID, PartnerID, Secret = keys.getDetails(account, server)
    
    baseString= url +'|'+ json.dumps(body)

    sig=HMAC(bytearray(Secret,'ASCII'), bytearray(baseString, 'ASCII'), sha256).hexdigest()
    
    header={
            "Content-Type":"application/json",
            "Authorization":sig
            }
    
    return url, header, body

def getResponse(url, body, account, server):
    
    url, header, body=getFields(url, body, account, server)

    result, response = APIConnect(url, header, json.dumps(body))
    
    return result, response
