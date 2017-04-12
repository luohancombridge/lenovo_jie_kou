# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
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
                    #判断是否有包含#的字段若果则执行python代码
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
class confi(object):
    #第一个参数为文件夹路径，第二个参数为需要执行js的网页句柄
    def __init__(self,*path_h):
            self.log=log()
            # 查找文件夹内各种配置文件路径，表格名和文件夹名相同，json.txt为json模板名，config为接口参数，第一个为url，第二个为头key，第三个为头value
            # 获取最后的目录名
            if len(path_h)==2:
                self.h=path_h[1]
                self.path=path_h[0]
            else:
                self.path = path_h[0]
            excel_name = os.path.basename(self.path)
            # 查找文件名，excel
            for dir, b, file in os.walk(self.path):
                # 返回表格路径
                for z in file:
                    if excel_name in z:
                        self.excel_path = os.path.join(self.path, z)
                    elif 'json' == z.split('.')[0]:
                        self.json_path = os.path.join(self.path, z)
                    elif 'config' == z.split('.')[0] :
                        self.config_path = [i.replace('\n','') for i in open(os.path.join(self.path, z)).readlines()]
            # 返回值第一个为表格路径，第二个为json路径，第三个为配置文件内容列表
            self.jiekou_detail =(self.excel_path, self.json_path, self.config_path)
    #f发送调用的实验用的接口，参数第一个为请求数据
    def  just_reque(self,data):
        self.req = self.creat_json(data)
        self.resulte = self.reque(self.req, self.config_path)
        return self.resulte
    #发送数据到前段及后台方法,第二个为要发送的数据字典
    def all_send(self,data):
        self.log.wri("all send类接受data数据 %s" % data)
        if 'json' in data.values():
            self.req=data['json']
        else:
          self.req=self.creat_json(data)
        self.log.wri("all send生成json后的数据 %s" % self.req)
        self.resulte=self.reque(self.req,self.config_path)
        self.log.wri("reque发出请求后接受的返回结果数据 %s" % self.resulte)
        #将结果发送到页面前段
        self.send_js(self.req,self.resulte)
        #将结果发送到后端
        k=self.req+'##'+self.resulte
        print 77777777777777777777777
        k1=self.req
        k2=self.resulte
        print type(k1)
        print type(k2)
        self.log.wri("all  send 发到后端的接口信息字符串 %s" % k)
        self.send(k)
        self.read_log()
    #读取json模板信息，并与传入参数匹配生成json字符串，第一个为模板路径，第二个要生成json的数据信息,返回匹配后的json字符串
    def creat_json(self,data):
        j = json.loads(open(self.json_path).read().decode('GB2312'))
        self.log.wri("creat_json 开始读取的json模板数据 %s" % j)
        self.log.wri("creat_json 获取的参数未处理 %s" % data)
        #判断是否有重复json
        #判断哪个键包含有二级参数
        keys=j.keys()
        er_ji='none'
        for i  in j:
            if type(j[i])==list and type(j[i][0])==dict:
                er_ji=j[i][0]
                keys = keys + er_ji.keys()
                break
            elif type(j[i])==dict:
                er_ji = j[i]
                keys = keys + er_ji.keys()

        #从二级判断是否包含有三级参数
        san_ji='none'
        if er_ji!='none':
                if type(er_ji) == list and type(er_ji[0]) == dict:
                    for i in er_ji[0]:
                        if  type(er_ji[0][i])==list and type(er_ji[0][i][0])==dict:
                              san_ji = er_ji[0][i][0]
                              keys = keys + san_ji.keys()
                              break
                        elif type(er_ji[0][i])==dict:
                            san_ji = er_ji[0][i]
                            keys = keys + san_ji.keys()
                            break
                elif type(er_ji) == dict:
                    for i in er_ji:
                        if type(er_ji[i]) == list and type(er_ji[i][0]) == dict:
                            san_ji = er_ji[i][0]
                            keys = keys + san_ji.keys()
                            break
                        elif type(er_ji[i]) == dict:
                            san_ji = er_ji[i]
                            keys = keys + san_ji.keys()
                            break


        #截止
        #删除表格中json不存在键
        self.s=j.keys()
        if er_ji != 'none':
            self.s=self.s+er_ji.keys()
        if san_ji != 'none':
            self.s=self.s+san_ji.keys()
        for i  in data.keys():
            if  i not in self.s:
                data.pop(i)
        for i in data.keys():
            if i in j.keys():
               if data[i]=='':
                   j.pop(i)
               elif type(j[i])==int:
                 if type(data[i]) == float:
                     data[i] = int(data[i])
                 j[i] = int(data[i])
               else:
                   if type(data[i])==float:
                       data[i]= str(int(data[i]))
                   j[i] =data[i]
            #没有三级参数
            elif er_ji!='none'  and san_ji=='none':
                if i in er_ji.keys():
                    if data[i] == '':
                        er_ji.pop(i)
                    elif type(er_ji[i]) == int:
                           er_ji[i]=int(data[i])
                    else:
                       er_ji[i] = data[i]
             # 有三级参数
            elif er_ji != 'none' and san_ji != 'none':
                if data[i] == '':
                    data.pop(i)
                elif i in san_ji.keys():
                    if type(san_ji[i]) == int:
                        san_ji[i] = int(data[i])
                    else:
                        san_ji[i] = data[i]
                elif i in er_ji.keys():
                        if type(er_ji[i]) == int:
                            er_ji[i] = int(data[i])
                        else:
                            er_ji[i] = data[i]
        for i in keys:
            if i in data.keys():
                pass
            else:
                if i in j.keys() and type(j[i]) not in [dict,list]:
                    print 22
                    print i
                    j.pop(i)
                if er_ji!='none' and i in er_ji.keys() and type(er_ji[i]) not in [dict,list]:
                    print 22
                    print i
                    er_ji.pop(i)
                if san_ji!='none' and i in san_ji.keys() and type(san_ji[i]) not in [dict,list]:
                    print 22
                    print i
                    san_ji.pop(i)
        self.log.wri("creat_json 最后处理完成json参数 %s" % j)
        self.dict_jreq=j
        x=json.dumps(j)
        return x
    #f发送调用的实验用的接口，参数第一个为请求数据，第二个为列表形式：第一个为url,第二个为头，第三个为头值
    def  reque(self,data,req):
        if req[2].strip()=='application/json':
           request = urllib2.Request(req[0],data)
           request.add_header(req[1],req[2])
           response = urllib2.urlopen(request)
           return response.read()
        elif 'x-www-form-urlencoded' in req[2].strip():
          request = urllib2.Request(req[0])
          request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
          if 'createStockItem'  in req[0] or 'autoOnlineDataCheck'  in req[0]:
              req_data = {"data": data}
          else:
              req_data=eval(data)
          self.log.wri("请求的json数据 %s" % req_data)
          response = urllib2.urlopen(request, urllib.urlencode(req_data))
          x=response.read()
          print 11111111111111111111111111111111111111111111111111111
          print x
          return x
    #执行js将json数据传送到页面上
    def send_js(self,req,pon):
       req=json.dumps(json.loads(req))
       self.log.wri("发送到前端的js请求 %s" % req)
       req=json.dumps(json.loads(json.dumps(demjson.decode(req)), parse_int=int), indent=4, sort_keys=False,
                  ensure_ascii=False).replace('"','\\"').replace('\n','\\n').replace('\\\\','\\')
       self.h.execute_script('$("#1").html("%s")'  % req)
       pon = json.dumps(json.loads(json.dumps(demjson.decode(pon)), parse_int=int), indent=4, sort_keys=False,
                        ensure_ascii=False).replace('"', '\\"').replace('\n', '\\n')
       self.h.execute_script('$("#2").html("%s")' % pon)
       self.h.execute_script('$("#yun1").html("%s")' % os.path.basename(self.path))
    #调用发送数据的接口
    def send(self,b):
        #发送服务器信息
        url = 'http://192.168.139.130:5021/linux_config'
        #倒数第二个个为接口配置信息，最后一个为目录信息
        request = urllib2.Request(url)
        request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
        data={'linux':open(os.path.join(self.path, 'linux.txt')).read()}
        data['config']=open(os.path.join(self.path, 'config.txt')).read()
        data['name'] = os.path.basename(self.path)
        response = urllib2.urlopen(request, urllib.urlencode(data))
        #发送接口信息
        url='http://192.168.139.130:5021/jiaobenshuru'
        data = b
        request = urllib2.Request(url)
        request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
        data={"data":b}
        data['name'] = os.path.basename(self.path)
        response = urllib2.urlopen(request, urllib.urlencode(data))
        response = urllib2.urlopen(request)
        time.sleep(2)
        print 11111111111111111111111111111111111111111111111111111
        print response.read()
    #读取日志
    def read_log(self):
        #发送服务器信息
        url = 'http://192.168.139.130:5021/read_logs'
        request = urllib2.Request(url)
        request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
        data={"name":os.path.basename(self.path)}
        try:
          response = urllib2.urlopen(request,urllib.urlencode(data))
          x=response.read().split('\n')
        except:
            print 22
        else:
            print x
        return 11
class log(object):
    def __init__(self):
        self.logger = logging.getLogger('mylogger')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(r'E:\httt_stock_last_jiaoben\log.txt')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    def wri(self,data):
        self.logger.info(data)
if __name__=='__main__':
    create_stock(r'C:\work\httt_stock_last_jiaoben\exe')
    #create_stock(r'E:\httt_stock_last_jiaoben\getStockList')
     #create_stock(r'E:\httt_stock_last_jiaoben\getStockDetail')
    # create_stock(r'E:\httt_stock_last_jiaoben\getStockAuditList')
   # create_stock(r'E:\httt_stock_last_jiaoben\stockAudit')
     #create_stock(r'E:\httt_stock_last_jiaoben\queryGoodsList')
    # create_stock(r'E:\httt_stock_last_jiaoben\getStockManageList')
    # create_stock(r'E:\httt_stock_last_jiaoben\acceptCISResult')
     #create_stock(r'E:\httt_stock_last_jiaoben\autoOnlineDataCheck')