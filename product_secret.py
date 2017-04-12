# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys

from paymax.config import PaymaxConfig
from paymax.config import SignConfig
from paymax.util.PaymaxUtil import *
from paymax.sign import RSASign
from paymax.exception import exception
import requests
from paymax.util.HttpUtil import *
from paymax.model.Charge import *
from paymax.config import PaymaxConfig
import json
from selenium import webdriver
import time
import chardet
import unittest
import demjson
import urllib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
#from  creat_dang import *
import unittest
import xlrd
import json
import urllib2
import os
import logging
body={'order_no':generate_uuid(),
            'amount':0.1,
            'subject':'测试subject',
            'body':'测试body',
            'channel':'alipay_app',
            'app':'app_7hqF2S6GYXET457i',
            'client_ip':'127.0.0.1',
            'currency':'CNY',
            'description':'description'}
body=json.dumps(body)
#header 头
header = setHeader()
#组装header
request_header = {'Host': header['Host'],
                  "Content-Type": "application/json;charset=utf-8",
                  'Authorization': header['Authorization'],
                  'nonce': header['nonce'],
                  'timestamp': header['timestamp'],
                  'sign': sign_data}
# 签名数据
sign_data = to_sign_data(header=header, method='post', uri=uri, body=body, )
k=ApiResource.request(uri='/v1/charges',body=body)
print  33333333
print k


