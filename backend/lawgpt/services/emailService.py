import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from lawgpt.log import get_logger
from lawgpt.config import settings

logger = get_logger(__name__)

class EmailSender:
    def __init__(self, smtp_server=settings.MAIL.HOST,
                 smtp_port=settings.MAIL.PORT,
                 sender_email=settings.MAIL.USERNAME,
                 sender_password=settings.MAIL.PASSWORD):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email: str, subject: str, message: str):
        # 创建一个MIMEMultipart对象来构建邮件
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # 添加邮件正文
        body = MIMEText(message, 'plain')
        msg.attach(body)

        # 使用SMTP发送邮件
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)