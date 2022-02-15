from calendar import c
import os
import smtplib
from email.mime.text import MIMEText

smtp_port = os.environ.get('smtp_port')
smtp_server = os.environ.get('smtp_server')
smtp_user = os.environ.get('smtp_user')
smtp_pass = os.environ.get('smtp_pass')

# smtp 연결을 만들고 로그인함
def make_connection():
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.ehlo()
    smtp.starttls() 
    smtp.login(smtp_user, smtp_pass)
    return smtp

# smtp 연결하고 보냄 ㅇㅇ
def send_email(mime, to):
    try:
        smtp = make_connection()
        smtp.sendmail(smtp_server, to, mime.as_string()) 
        smtp.quit()
        return True
    except:
        return False