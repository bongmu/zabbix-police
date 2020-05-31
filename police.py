#!/usr/bin/env python
#coding:utf-8
import redis
import sys
subject=sys.argv[1]
# *需要修改的主机
r = redis.StrictRedis(host="*******", password="123456", port=6379)
print subject
r.set(subject,subject)
