# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 12:10:53 2017

@author: woon.zhenhao
"""

from cx_Freeze import setup, Executable
import sys
#import os
import codecs

#os.environ['TCL_LIBRARY'] = r'C:\Users\ASUS\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
#os.environ['TK_LIBRARY'] = r'C:\Users\ASUS\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable(script="shopeemain.py")]

packages = ['idna','codecs','time','datetime','keys','apiconnector','ordermanagement','prodmanagement','masterReader','log','json','pandas','os','math','openpyxl','requests','hashlib','hmac', 'numpy']
#includes=['keys.py','apiconnector.py','ordermanagement.py','prodmanagement.py','masterReader.py','log.py']
includes=[]

options = {
    'build_exe': {
        'packages':packages,
        'include_files':includes
    },
}

setup(
    name = "zhen hao",
    options = options,
    version = "1",
    description = 'shopee connector',
    executables = executables
)