# -*- coding: utf-8 -*-
#处理excel表格中的特殊数据
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
class excel_data_exe(object):
    # 处理excel表格中的特殊数据,带#的为要运行的代码数据，必须有一个返回值
    def han_shu(self,data):
        self.b = 'self.a='
        exec (self.b + data.split('##')[1])
        return self.a