# “不错”订阅系统

本系统是基于python的邮件订阅系统，原理是使用`bs4`和`requests`库爬取订阅网站最新通知，并使用`smtplib`和`email`库发送邮件到指定邮箱。

目前该系统使用邮箱域名为mail.zzy2001.com，仅支持安徽大学（主网站、教务处、及各学院）的通知爬取。未来将支持更多订阅源。

本系统代码开源，采用CC协议。
