#!/usr/bin/env python
#coding:utf-8
import MySQLdb
import redis
import sys
from dbread import *
from operation import *
from weixin import *
import datetime,time
import config


sendtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
# 获取企业微信的告警token
accesstoken = gettoken()
#print accesstoken


#发送微信给运维人员
users=config.alarm_users
#在zabbix 可以找到告警收敛的动作ID（actionid）
actionid=config.action_id
#连接redis，并读取所有事件id
r = redis.StrictRedis(host=config.redis_host, password=config.redis_pass, port=config.redis_port)


subjectlist=r.keys()

print "============%s===========" % sendtime
print "event id:"
print subjectlist
print "========================="

for i in subjectlist:
    r.delete(i)
#r.flushdb()



#获取原始数据并存入数据库
originallist=[]
for subject in subjectlist:
	# 获取数据库返回的结果
        messagedict=alerts_eventid(str(actionid),subject)
        originallist.append(messagedict)

# print originallist

problem=mergeproblem(originallist)
normal=mergenormal(originallist)



#发送告警信息
messagelist=compressproblem(problem)

if len(messagelist) != 0:
    for content in  messagelist:
        print sendtime
        for user in users:
            senddata(accesstoken,user,content)


#发送恢复信息    
messagelist=compressnormal(normal)

if len(messagelist) != 0:
    for content in  messagelist:
        print sendtime
        for user in users:
            senddata(accesstoken,user,content)
