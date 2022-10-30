# -*- coding: utf-8 -*-
from datetime import date, timedelta
import requests
import smtplib
from email.mime.text import MIMEText
import yaml
from json import dumps
import os


def get_next_next_days(offset):
    # 今天日期
    today = date.today()
    # 今天周几，1-6周一到周六，0周日
    weekday = int(today.strftime('%w'))
    next3 = ((3 - weekday) if weekday <= 3 else (10 - weekday)) + offset
    next4 = ((4 - weekday) if weekday <= 4 else (11 - weekday)) + offset
    return ['', '', '', (today + timedelta(next3)).strftime('%Y-%m-%d'), (today + timedelta(next4)).strftime('%Y-%m-%d')]

def send(content, receivers, mail_host, port, mail_user, mail_pass):
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = '拍照预约有啦！'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = ','.join(receivers)
    # 登录并发送邮件
    try:
        # 连接到服务器
        smtpObj = smtplib.SMTP_SSL(mail_host, port)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        # 打印错误
        print('error', e)

day_name = ['', '', '', '三', '四']

# 查询url
baseurl = 'https://apixy.xingying2018.com/api/WebChatAppointment/GetAppointmentList'
# 预约url
addurl = 'https://apixy.xingying2018.com/api/WebChatAppointment/AddAppointment'

# headers
headers = {
    "Origin": "https://weixinzj.xingying2018.com",
    "Content-Type": "application/json"
}

# params
typeid = 2  # 2是普通拍摄，1是精品
# offset 控制下周还是下下周
offset = [0, 7]
# 邮件内容
content = ''
cfg = dict()
with open(os.path.dirname(__file__) + '/config.yml', encoding='utf-8', mode='r') as f:
    
    # 读取配置文件
    cfg = yaml.safe_load(f)
    mail_host = cfg['mail']['sender']['host']
    mail_user = cfg['mail']['sender']['user']
    mail_pass = cfg['mail']['sender']['password']
    sender = cfg['mail']['sender']['address']
    port = cfg['mail']['sender']['port']
    receivers = cfg['mail']['receivers']
    plan = cfg['plan']
    # 发送请求, offset控制拿哪一周的数据
    for o in offset:
        dt = get_next_next_days(o)  # 获取周三和周四的日期

        # 周三的url
        url3 = baseurl + '?typeid=' + str(typeid) + '&dt=' + dt[3]
        # 周四的url
        url4 = baseurl + '?typeid=' + str(typeid) + '&dt=' + dt[4]

        url = ['', '', '', url3, url4]
        for i in range(3, 5): # 依次获取周三和周四
            content = ''
            data = requests.get(url[i], headers=headers).json()
            if data['statusCode'] == 201:
                print('周' + day_name[i] + '(' + dt[i] + '):' + data['message'])
            elif data['statusCode'] == 200: # 成功获取到数据
                cnt = 0
                for item in data['data']['appointmentdata']: # 遍历这一天所有可以预约的时间段
                    id = item['id']
                    appointCount = item['appointCount']
                    appointNum = item['appointNum']
                    dateSlot = item['dateSlot']
                    # 还有剩余人数
                    if appointCount > appointNum:
                        cnt += 1
                        content += '周' + day_name[i] + '(' + dt[i] + ')' + '时间段：' + dateSlot + '剩余' + str(
                            appointNum - appointCount) + '名额(' + str(appointCount) + '/' + str(appointNum) + ')\n'
                        # 在配置文件中寻找想要预约这个事件段的人
                        for p in plan:
                            time_map = p['time']
                            # 存在于预约计划并且还没预约过
                            if dt[i] in time_map and dateSlot in time_map[dt[i]] and p['success'] == False:
                                json_data = {
                                    "ID": id,
                                    "OpenID": p['openid'],
                                    "DateSlot": dateSlot,
                                    "AppointDate": dt[i]
                                }
                                res_data = requests.post(addurl, data=dumps(json_data), headers=headers).json()
                                if res_data['statusCode'] == 200:
                                    print('为 ' + p['name'] + ' 预约（' + dt[i] + ' ' + dateSlot + '）成功，开始发送邮件')
                                    send('预约成功：' + dt[i] + ' ' + dateSlot, [p['mail']], mail_host, port, mail_user, mail_pass)
                                    # 稍后会写入配置文件
                                    p['success'] = True
                                    print('邮件发送成功，返回数据为：')
                                    print(res_data)

                if 0 == cnt:
                    print('周' + day_name[i] + dt[i] + ':' + '全都已满')
            else:
                print('出现未知错误')
            # 发送邮件，同一天的只会发送一次
            if content != '' and not (dt[i] in cfg['mail']['sent']):
                send(content, receivers, mail_host, port, mail_user, mail_pass)
                cfg['mail']['sent'].append(dt[i])
                

    


with open(os.path.dirname(__file__) + '/config.yml', encoding='utf-8', mode='w') as f:
    yaml.dump(cfg, f)
