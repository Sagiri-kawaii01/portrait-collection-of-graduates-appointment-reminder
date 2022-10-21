# -*- coding: utf-8 -*-
from datetime import date, timedelta
import requests
import smtplib
from email.mime.text import MIMEText


def get_next_next_days(offset):
    # 今天日期
    today = date.today()
    # 今天周几，1-6周一到周六，0周日
    weekday = int(today.strftime('%w'))
    next3 = (3 - weekday) if weekday <= 3 else (10 - weekday) + offset
    next4 = (4 - weekday) if weekday <= 4 else (11 - weekday) + offset
    return ['', '', '', (today + timedelta(next3)).strftime('%Y-%m-%d'), (today + timedelta(next4)).strftime('%Y-%m-%d')]

day_name = ['', '', '', '三', '四']

# 设置服务器所需信息
# 163邮箱服务器地址，其他邮箱也可以，但是QQ邮箱有个额外的验证
mail_host = 'smtp.163.com'
# 163用户名
mail_user = 'lgz1104738025'
# 密码(部分邮箱为授权码)
mail_pass = 'UGTACYYAULPISHXG'
# 邮件发送方邮箱地址
sender = 'lgz1104738025@163.com'
# 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['1104738025@qq.com', '1135664656@qq.com']


# url
baseurl = 'https://apixy.xingying2018.com/api/WebChatAppointment/GetAppointmentList'

# headers
headers = {
    "Origin": "https://weixinzj.xingying2018.com"
}

# params
typeid = 2  # 2是普通拍摄，1是精品
# offset 控制下周还是下下周
offset = [0, 7]


content = ''
# 发送请求
for o in offset:
    dt = get_next_next_days(o)  # 获取下下一个周三和周四

    # 下一个周三的url
    url3 = baseurl + '?typeid=' + str(typeid) + '&dt=' + dt[3]
    # 下一个周四的url
    url4 = baseurl + '?typeid=' + str(typeid) + '&dt=' + dt[4]

    url = ['', '', '', url3, url4]
    for i in range(3, 5):
        data = requests.get(url[i], headers=headers).json()
        if data['statusCode'] == 201:
            print('周' + day_name[i] + dt[i] + ':' + data['message'])
        elif data['statusCode'] == 200:
            cnt = 0
            for item in data['data']['appointmentdata']:
                appointCount = item['appointCount']
                appointNum = item['appointNum']
                dateSlot = item['dateSlot']
                if appointCount < appointNum:
                    cnt += 1
                    content += '周' + day_name[i] + '(' + dt[i] + ')' + '时间段：' + dateSlot + '剩余' + str(
                        appointNum - appointCount) + '名额(' + str(appointCount) + '/' + str(appointNum) + ')\n'
            if 0 == cnt:
                print('周' + day_name[i] + dt[i] + ':' + '全都已满')
        else:
            print('出现未知错误')

# 发送邮件
if content != '':
    # 设置email信息
    # 邮件内容设置
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
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
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

