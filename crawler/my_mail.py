#coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from crawler.config import MAIL_PASSWORD,MAIL_SERVER,MAIL_USERNAME,ADMINS


def mail(sender=MAIL_USERNAME, password=MAIL_PASSWORD, receiver=ADMINS[0], msg_text='运行失败',
         msg_from=MAIL_USERNAME, msg_to = ADMINS[0], msg_subject='警报', server_smtp=MAIL_SERVER, server_port=465):
    '''
    :param sender: 发件人邮箱地址
    :param password: 发件人邮箱密码
    :param receiver: 收件人邮箱（可以发送给自己)
    :param msg_text: 邮件文本内容（字符串）
    :param msg_from: 发件人邮箱昵称（字符串）
    :param msg_to: 收件人邮箱昵称(字符串）
    :param msg_subject: 邮件的主题，也可以说是标题
    :param server_smtp: 发件人邮箱中的SMTP服务器
    :param server_port: 发件人邮箱中的SMTP服务器端口
    :return:
    '''
    ret = True
    try:
        msg = MIMEText(msg_text, 'plain', 'utf-8')
        msg['From'] = formataddr([msg_from, sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([msg_to, receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = msg_subject  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(server_smtp, server_port)  # 发件人邮箱中的SMTP服务器，端口
        server.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(sender, [receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret



if __name__ == '__main__':
    import random
    from crawler.db_handler import db

    house_counts = 5000
    is_crawler_counts = db.get_counts()
    msg_text = "成功爬取%d条, 已经爬取到%d条" % (house_counts, is_crawler_counts)
    msg_subject = 'house_data_crawler'



    ret = mail(msg_text= msg_text, msg_subject= msg_subject)
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
    print(random.uniform(0.05,0.1))