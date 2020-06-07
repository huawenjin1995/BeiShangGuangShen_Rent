#coding: utf-8
import os
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from crawler.config import MAIL_PASSWORD,MAIL_PORT,MAIL_SERVER,MAIL_USE_TLS,MAIL_USERNAME,ADMINS

logger = logging.getLogger(__name__)
# 为日志对象添加一个SMTPHandler的实例：
if MAIL_SERVER:
    auth = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        auth = (MAIL_USERNAME, MAIL_PASSWORD)
    secure = None
    if MAIL_USE_TLS:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(MAIL_SERVER, MAIL_PORT),
        fromaddr=MAIL_USERNAME,
        toaddrs=ADMINS,
        subject='house_data_crawler failed',
        credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    logger.addHandler(mail_handler)

# 启用另一个基于文件类型RotatingFileHandler的日志记录器
if not os.path.exists('logs'):
    os.mkdir('logs')
    # 日志文件的存储路径位于顶级目录下，相对路径为logs/house_data_crawler.log，
    # 如果其不存在，则会创建它。
file_handler = RotatingFileHandler('logs/house_data_crawler.log', maxBytes=102400,
                                   backupCount=30)
# 日志文件大小限制为100k，保留最后30个日志文件作为备份
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: [in %(pathname)s:%(lineno)d] %(message)s'))
# 设置日志消息格式，依次为：时间戳、日志记录级别、消息以及日志来源的源代码文件和行号。
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
