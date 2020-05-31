#!/usr/bin/python
#coding=utf-8
import datetime,time
import sys
import json
import config

reload(sys)
sys.setdefaultencoding('utf8') 


#告警合并
def mergeproblem(originallist):
    problemlist=[]
    normalist=[]
    Unknown=[]
    triggerkeylist=[]
    sorts=[]
    alarminfo=[]
    #告警or恢复
    for origina in originallist:
	# print origina['triggervalue']

        if origina['triggervalue'] == '1' :            
            problemlist.append(origina)
            if origina['triggerkey'] not in triggerkeylist:
                triggerkeylist.append(origina['triggerkey'])
        else :
            Unknown.append(origina)

    for triggerkey in triggerkeylist:
        for problem in problemlist:
            if problem['triggerkey'] == triggerkey:
                sorts.append(problem)
        alarminfo.append(sorts)
        sorts=[]

    return alarminfo
#恢复合并
def mergenormal(originallist):
    normallist=[]
    Unknown=[]
    triggerkeylist=[]
    sorts=[]
    alarminfo=[]
    #告警or恢复
    for origina in originallist:

        if origina['triggervalue']=='0' :            
            normallist.append(origina)
            if origina['triggerkey'] not in triggerkeylist:
                triggerkeylist.append(origina['triggerkey'])
        else :
            Unknown.append(origina)

    for triggerkey in triggerkeylist:
        for normal in normallist:
            if normal['triggerkey']==triggerkey:
                sorts.append(normal)
        alarminfo.append(sorts)
        sorts=[]
    return alarminfo

#告警压缩
def compressproblem(alarminfo):
    # print "alarminfo:", alarminfo
    currenttime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    messagelist=[]

    for info in alarminfo:
        hostlist=''
        hostgroup=''
        infonum=len(info)

        for host in info:
	    # print json.dumps(host,sort_keys=True,indent=4)
            triggername = host['triggername']
            # hostinfo=host['hostname']+':'+host['ipaddress']+'\n'
            hostinfo = host['ipaddress']+'\n'

            if host['hostgroup'] not in hostgroup:
                hostgroup += host['hostgroup']+'\n'
            hostlist += hostinfo

	# 设定告警条数 超过多少条 就压缩
        if infonum >= 1 and infonum <= config.alarm_count:        
            # message = '告警◕﹏◕\n' + '告警主机: ' + str(infonum) + '台\n' + hostlist + '涉及主机组: ' + hostgroup + '告警项目: ' + triggername + '\n' + '故障时间: ' + currenttime
            message = '告警◕﹏◕\n\n' + '告警主机: ' + str(infonum) + '台\n' + hostlist + '告警项目:\n' + triggername + '\n' + '故障时间: ' + currenttime
            messagelist.append(message)

        elif infonum > config.alarm_count:
            # message = '告警◕﹏◕\n' + '当前存在大量相同告警项, 详情请查看Zabbix系统！\n' + '告警主机: ' + str(infonum) + '台\n' + '告警项目: ' + triggername + '\n' + '故障时间: ' + currenttime
            message = '告警◕﹏◕\n\n' + '当前存在大量相同告警项, 详情请查看Zabbix系统！\n' + '告警主机: ' + str(infonum) + '台\n' + '告警项目:\n' + triggername + '\n' + '故障时间: ' + currenttime
            messagelist.append(message)
    return messagelist


#恢复压缩
def compressnormal(alarminfo):
    currenttime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    messagelist=[]
    for info in alarminfo:
        hostlist=''
        hostgroup=''
        infonum=len(info)
        for host in info:
            triggername=host['triggername']
            # hostinfo=host['hostname']+':'+host['ipaddress']+'\n'
            hostinfo = host['ipaddress']+'\n'
	
            if host['hostgroup'] not in hostgroup:
                hostgroup+=host['hostgroup']+'\n'
            hostlist+=hostinfo

        if infonum >= 1 and infonum <= config.alarm_count:        
            message = '恢复◕‿◕\n\n' + '恢复主机: '+ str(infonum) + '台\n' + hostlist + '恢复项目:\n' + triggername + '\n' + '恢复时间: ' + currenttime
            messagelist.append(message)
        elif infonum > config.alarm_count:
            message = '恢复◕‿◕\n\n' + '大量主机已经恢复!\n' + '恢复主机: ' + str(infonum) + '台\n' + '恢复项目:\n' + triggername + '\n' + '恢复时间: ' + currenttime
            messagelist.append(message)
    return messagelist
