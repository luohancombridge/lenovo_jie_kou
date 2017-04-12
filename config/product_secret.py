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

class product_code(object):
    def setHeader(self):
        nonce = generate_uuid()
        timestamp = generate_timestamp()
        header = {
            "Host": "www.paymax.cc",
            "ContentType": "application/json;charset=utf-8",
            "nonce": nonce,
            "timestamp": timestamp,
            "Authorization": SignConfig.PAYRIGHT_SECRET_KEY
        }
        return header

