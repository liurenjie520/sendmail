#!/usr/bin/env python3
# coding: utf-8


import smtplib  # 加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class SendMail(object):
    def __init__(self,sender,title,content):
        self.sender = sender  #发送地址
        self.title = title  # 标题
        self.content = content  # 发送内容
        self.sys_sender = 'iamliurenjie@163.com'  # 系统账户
        self.sys_pwd = ''  # 系统账户密码

    def send(self,file_list):
        """
        发送邮件
        :param file_list: 附件文件列表
        :return: bool
        """
        try:
            # 创建一个带附件的实例
            msg = MIMEMultipart()
            # 发件人格式
            msg['From'] = formataddr(["技术服务部", self.sys_sender])
            # 收件人格式
            msg['To'] = formataddr(["", self.sender])
            # 邮件主题
            msg['Subject'] = self.title

            # 邮件正文内容
            msg.attach(MIMEText(self.content, 'plain', 'utf-8'))

            # 多个附件
            for file_name in file_list:
                print("file_name",file_name)
                # 构造附件
                xlsxpart = MIMEApplication(open(file_name, 'rb').read())
                # filename表示邮件中显示的附件名
                xlsxpart.add_header('Content-Disposition','attachment',filename = '%s'%file_name)
                msg.attach(xlsxpart)

            # SMTP服务器
            server = smtplib.SMTP_SSL("smtp.163.com", 465,timeout=10)
            # 登录账户
            server.login(self.sys_sender, self.sys_pwd)
            # 发送邮件
            server.sendmail(self.sys_sender, [self.sender, ], msg.as_string())
            # 退出账户
            server.quit()
            return True
        except Exception as e:
            print(e)
            return False

if __name__ == '__main__':
    # 发送地址
    sender = "iamliurenjie@gmail.com"
    # 标题
    title = "统计"
    # 发送内容
    content = "2019-11-01 ~ 2019-11-30 统计，见附件!"
    # 附件列表
    file_list = ["黄历.ics","yj2021.json"]
    ret = SendMail(sender, title, content).send(file_list)
    print(ret,type(ret))