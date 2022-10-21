#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 13:19
# @Author  : lgz
# @FileName: test.py
# @Software: PyCharm
# @Blog    : https://www.cnblogs.com/jvav/
# @Github  : https://github.com/Wfo-12
import yaml
import requests
import json
cfg = dict()
addurl = 'https://apixy.xingying2018.com/api/WebChatAppointment/AddAppointment'

# headers
headers = {
    "Origin": "https://weixinzj.xingying2018.com",
    "Content-Type": "application/json"
}
with open('config.yml', encoding='utf-8', mode='r') as f:
    cfg = dict(yaml.safe_load(f))
    plan = cfg['plan'][0]
    data = {
        "ID": 'cc8ea03ba2e54326b30ad3385aecc62f',
        "OpenID": plan['openid'],
        "DateSlot": plan['time'],
        "AppointDate": plan['date']
    }
    response = requests.post(url=addurl, headers=headers, data=json.dumps(data))
    print(response.json())
with open('config.yml', encoding='utf-8', mode='w') as f:
    yaml.dump(cfg, f)
