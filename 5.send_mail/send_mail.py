#! /usr/bin/env python
# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import smtplib
import requests
import json


# 当前日期的后（前）几天的日期
sender = 'qq_number@qq.com'
receivers = ["qq_number@qq.com"]

base_url = "http://0.0.0.0:5000"


def signin(username, password):
    url = "%s/token/user/signin" % base_url
    payload = {'account': username, 'password': password}
    headers = {"Content-Type": "application/json"}
    result = requests.post(url=url, headers=headers, data=json.dumps(payload))
    r_json = json.loads(result.text)
    assert r_json["code"] == 200, r_json
    return r_json["body"]["token"]


def get_date(days):
    import datetime
    import pytz
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        date = now + datetime.timedelta(days=days)
    except Exception as e:
        raise e
    return date.strftime('%Y-%m-%d')


def send_email_with_pingan_smtp(content, sender, recivers):
    date = get_date(-1)
    mail_host = "your_mail_host"
    mail_port = 25

    try:
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header("众包后台", "utf-8")
        message['To'] = Header("众包运营", "utf-8")
        message['Subject'] = Header("{0}日众包运营情况".format(date), "utf-8")

        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, mail_port)
        smtpObj.sendmail(sender, recivers, message.as_string())

        print("send email successfully")
    except smtplib.SMTPException as e:
        print(e.message)
        print("fail to send email")


def send_email_with_SSL(content, sender, receivers):
    qq_host = "smtp.qq.com"
    qq_port = 465
    mail_user = "qq_number@qq.com"
    mail_pass = "your_mail_key"
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["众包后台", mail_user])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["众包运营", receivers[0]])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "众包运营情况"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(qq_host, qq_port)
        server.login(mail_user, mail_pass)
        server.sendmail(sender, receivers, msg.as_string())
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(e.message)
        print("邮件发送失败")


def get_data_from_crowdsourcing():
    try:
        username = 'phone number'
        password = 'your password'
        str_token = signin(username, password)
    except Exception as e:
        print("can't signin ,error : " + e.message)
        raise Exception("can't signin ,error : " + e.message)
    try:
        url = "{0}/token/your_url" .format(base_url)
        headers = {
            "Content-Type": "application/json",
            "Authorization": str_token}
        result = requests.post(url=url, headers=headers)
        r_json = json.loads(result.text)
        assert r_json["code"] == 200, r_json
        date = r_json["body"]["date"]
        total_user = r_json["body"]["total_user"]
        date_new_users = r_json["body"]["date_new_users"]
        activate_users = r_json["body"]["activate_users"]
        date_job_users = r_json["body"]["date_job_users"]
        total_task_runs = r_json["body"]["total_task_runs"]
        yesterday_score = r_json["body"]["yesterday_score"]
        max_online_user = r_json["body"]["max_online_user"]
        max_online_task_run = r_json["body"]["max_online_task_run"]
        report_address = r_json["body"]["report_address"]
        content = '''尊敬的xx您好，
        昨日:{0}众包运营的数据为:
	    1. 用户总数:{1}
	    2. 当日新增:{2}
	    3. 日活跃用户数:{3}
	    4. 日作业用户数:{4}
	    5. 日平台完成:{5}
	    6. 昨日积分发放数:{6}
	    7. 高峰时段在线人数:{7}
	    8. 高峰时段Max任务数:{8}
	    9. BI报告地址:{9}
        '''.format(
            date,
            total_user,
            date_new_users,
            activate_users,
            date_job_users,
            total_task_runs,
            yesterday_score,
            max_online_user,
            max_online_task_run,
            report_address)
        return content
    except Exception as e:
        print("can't get data from crowdsourcing platform: " + e.message)
        raise Exception("can't signin ,error : " + e.message)


if __name__ == '__main__':
    # send_email("content",sender=sender,recivers=receivers)
    content = get_data_from_crowdsourcing()
    # send_email_with_pingan_smtp(content,sender,receivers)
    send_email_with_SSL(content, sender, receivers)
