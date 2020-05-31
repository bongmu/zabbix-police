#!/usr/bin/python
# coding: utf-8
#python2将zabbix报警信息发送到微信。
#脚本中*****需要修改的地方

import urllib,urllib2
import json
import sys
import config


def gettoken():
    CropID='*********'
    Secret='**************-*****'
    GURL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+CropID+"&corpsecret="+Secret
    token_file = urllib2.urlopen(GURL)
    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token

def senddata(access_token,user,content):
    PURL="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+access_token
    send_values = {
        "touser":user,    #企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
        "toparty":"2",    #企业号中的部门id
        "msgtype":"text",  #消息类型
        "agentid":"********",  #填写企业号中的应用id，
        "text":{
            "content":content
           },
        "safe":"0"
        }
    send_data = json.dumps(send_values, ensure_ascii=False, indent=4).encode("utf-8")
    send_request = urllib2.Request(PURL, send_data)
    response = json.loads(urllib2.urlopen(send_request).read())
    print str(response)

if __name__ == '__main__':
    user = str(sys.argv[1])   #zabbix传过来的第一个参数
    content = str(sys.argv[3])  #zabbix传过来的第三个参数
    accesstoken = gettoken()
    senddata(accesstoken,user,content)
