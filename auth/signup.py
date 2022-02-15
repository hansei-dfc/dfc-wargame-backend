import os
from flask import Blueprint, request
from api import make_packet
from auth.db.email_verify import send_verify_email
from auth.db.users import create_user, is_user_exists_email
from regex import verify_email, verify_password

signup = Blueprint('signup', __name__)

@signup.route('/auth/signup', methods=["post"])
def on_signup():
    body = request.form
    
    if (not body or "name" not in body or "email" not in body or "password" not in body): 
        return make_packet(400, "데이터 빠짐 ㅅㄱ")

    name = body["name"].strip()
    email = body["email"].strip()
    password = body["password"]
    
    if (len(name) < 2 or not verify_email(email) or not verify_password(password)):
        return make_packet(400, "올바른 이멜 또는 비번 또는 이름 아님 ㅅㄱ")

    if (is_user_exists_email(email)): 
        return make_packet(400, "이미 있음 ㅅㄱ")

    id = create_user(name, email, password)
    if (send_verify_email(id, email)):
        return make_packet(200, "이멜 인증 ㄱ")
    else:
        return make_packet(400, "이메일 못보냈음 ㅇㅇ")
