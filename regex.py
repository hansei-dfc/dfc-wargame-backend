import re

email_regex = re.compile("^([\w\.\_\-])*[a-zA-Z0-9]+([\w\.\_\-])*([a-zA-Z0-9])+([\w\.\_\-])+@([a-zA-Z0-9]+\.)+[a-zA-Z0-9]{2,8}$")
# 비밀번호 8자 하나의 문자 하나의 숫자
password_regex = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

def verify_email(str):
    return email_regex.match(str)

def verify_password(str):
    return password_regex.match(str)