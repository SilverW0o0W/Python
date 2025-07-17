#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: 
@create: 2025/7/17
@brief:
"""

# 发送带附件的邮件
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email_with_attachment(smtp_server, smtp_port, username, password, to_email, subject, body, attachment_path):
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain'))

    # 遍历附件文件夹内文件 并批量添加附件
    attachment_files = [os.path.join(attachment_path, f) for f in os.listdir(attachment_path)]

    for file_path in attachment_files:
        # 校验文件扩展名 PDF、DOC、DOCX、TXT、RTF、HTM、HTML、PNG、GIF、JPG、JPEG、BMP、EPUB
        if not file_path.lower().endswith(('.pdf', '.doc', '.docx', '.txt', '.rtf', '.htm', '.html', '.png', '.gif', '.jpg', '.jpeg', '.bmp', '.epub')):
            continue

        if os.path.isfile(file_path):  # 确保是文件而不是目录
            add_attachment(msg, file_path)

    # 发送邮件
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # 启用TLS加密
        server.login(username, password)
        server.send_message(msg)


def add_attachment(msg, file_path):
    """
    添加附件到邮件消息中
    :param msg: MIMEMultipart 邮件消息对象
    :param attachment_path: 附件文件路径
    """
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        # 添加附件头信息 处理附件名中文乱码
        part.add_header('Content-Disposition','attachment', filename=('utf-8', '', Header(file_path.split("/")[-1], 'utf-8').encode()))
        msg.attach(part)


if __name__ == '__main__':
    smtp_server = 'smtp.qq.com'
    smtp_port = 587
    username = ''
    password = ''
    to_email = ''
    subject = 'Book'
    body = ''
    attachment_path = 'book'
    send_email_with_attachment(smtp_server, smtp_port, username, password, to_email, subject, body, attachment_path)
