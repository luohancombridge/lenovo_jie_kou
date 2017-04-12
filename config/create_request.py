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
class create_stock(object):
    def __init__(self,path):
        self.h = webdriver.Chrome()
        time.sleep(3)
        self.h.get('http://192.168.139.130:5021/ceshi')
        self.send = confi(path,self.h)
        #self.query = confi(r'E:\httt_stock_last_jiaoben\queryPriceDetail')
        self.data = xlrd.open_workbook(self.send.excel_path)
        self.table = self.data.sheets()[0]
        self.key=self.table.row_values(0)
        self.data0 = [self.table.row_values(i) for i in range(1,self.table.nrows)]
        #self.creat_json(open(self.dir[1]).read())
        while True:
            time.sleep(1)
            try:
               self.data = xlrd.open_workbook(self.send.excel_path)
            except IOError:
                time.sleep(1)
                self.data = xlrd.open_workbook(self.send.excel_path)
            self.table = self.data.sheets()[0]
            self.data=[self.table.row_values(i) for i in range(1,self.table.nrows)]
            self.change={}
            if self.data0!=self.data:
              for k,i in enumerate(self.data):
                #增加数据行
                if len(self.data)!=len(self.data0):
                    self.data0 = self.data
                    self.data=self.data=dict(zip(self.key,self.data[-1]))
                    for k, i in enumerate(self.data.keys()):
                      if type(i) == float:
                        self.data[int(i)] = self.data.pop(i)
                # 生成json字符串
                    self.send.all_send(self.data)
                    break
                #修改数据行值
                elif self.data[k]!=self.data0[k]:
                   self.data0=self.data
                   #获取改变了信息的行信息字典形式
                   self.data=dict(zip(self.key,self.data[k]))
                   #调用查询价格单接口
                   #self.query_data=self.query.just_reque(self.data)
                   #self.s=json.loads(self.query_data)['result']['data'][0]['barcode']
                   #self.data['apiSign']=self.s
                   #读取excel有可能将数字键变为flaot，因此要将float键变成str整形
                   for k, i in enumerate(self.data.keys()):
                       if type(i) == float:
                           self.data[int(i)] = self.data.pop(i)
                   #生成json字符串
                   self.send.all_send(self.data)
                   break