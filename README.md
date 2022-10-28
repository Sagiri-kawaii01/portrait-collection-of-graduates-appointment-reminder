# 浙江省毕业生人像采集预约提醒，杭州新华社



[![Github stars](https://img.shields.io/github/stars/Sagiri-kawaii01/portrait-collection-of-graduates-appointment-reminder?logo=github)](https://github.com/Sagiri-kawaii01/portrait-collection-of-graduates-appointment-reminder)  [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![](https://img.shields.io/badge/Python-%3E%3Dv3.0-blue)



预约公众号为：浙江高校影像

需要先去公众号填写个人信息

官方只提供下一周的预约开放。当你发现的时候基本上都满了。



这个脚本的作用是自动检测，当发现预约开放时发送邮件提醒，**也可以配置自动预约**

可以部署到自己的服务器定时执行

> 配置文件实例 

```yaml
mail:
  # 接受者邮箱，可多个
  receivers:
  - 12345@qq.com
  - 54321@qq.com
  # 发送邮箱配置，这里只给个例子，请配置成自己的
  sender:
    # 发送邮箱地址
    address: 12345@163.com
    # 发送邮箱服务器地址，不建议QQ邮箱，QQ多一层验证
    host: smtp.163.com
    # 发送邮箱授权码（非密码）
    password: xiaoheizi
    # 发送邮箱服务器端口，163的是465
    port: 465
    # 发送邮箱账号
    user: zhiyinnitaimei
  sent:
  # 不用修改，由脚本自动控制，作用是控制邮件只发送一次
  - 2022-10-26
# 预约计划，支持多个
plan:
- mail: 12345@qq.com # 通知邮箱
  openid: abcd # openid，需自己抓包
  success: false # false表示还未预约
  time: # 计划预约的时间段，按顺序预约，最多预约一个
    '2022-11-02': # key为打算预约的日期
    - 11:00-11:30 # value是数组，值为时间段，时间段参考小程序
    - 13:30-14:00
    '2022-11-03':
    - 9:30-10:00
- mail: 54321@qq.com
  openid: gggg
  success: false
  time: 
    '2022-11-03':
    - 11:00-11:30
    - 15:30-16:00


```
