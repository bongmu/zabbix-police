#!/usr/bin/env python
#coding:utf-8
import MySQLdb
import redis
import sys
from dbread import *
from operation import *
from weixin import *
import datetime,time
sendtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
# 获取企业微信的告警token
accesstoken = gettoken()
#print accesstoken


#发送微信给运维人员
users=['all']
#在zabbix 可以找到告警收敛的动作ID（actionid）
actionid=11
#连接redis，并读取所有事件id
r = redis.StrictRedis(host="********", password="123456", port=6379)


r.delete("")
subjectlist=r.keys()


print subjectlist

for i in subjectlist:
    r.delete(i)
#r.flushdb()
