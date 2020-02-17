from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from smtplib import SMTP_SSL
import os

host_server = 'smtp.qq.com'
sender_qq = '**your qq ID**'
pwd = '**your password**'
sender_qq_mail = '**your mail address@qq.com**'

receiver = input('reciver address: ')
mail_content = input('email content: \n')
mail_attach_path = input('file path: ')
mail_title = input('email title: ')
msg = MIMEMultipart()
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = receiver
msg.attach(MIMEText(mail_content,'plain','utf-8'))
if len(mail_attach_path)>0:
    if os.path.exists(mail_attach_path):
        with open(mail_attach_path,'rb') as f:
            file_type = mail_attach_path.split('.')[-1]
            file_name = mail_attach_path.split('/')[-1]
            mime = MIMEBase(file_type,file_type,filename=file_name)
            mime.add_header('Content-Disposition', 'attachment', filename=file_name)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
        encoders.encode_base64(mime)
    else:
        raise Exception('No file in this path!')
    msg.attach(mime)

smtp = SMTP_SSL(host_server)
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)

smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()
