import os
from flask import Blueprint, request
from api import make_packet
from db import db
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

    conn = db()
    if(conn.cursor().execute("select exists(select 1 from `users` where email=@E)", email) != -1):
        conn.close()
        return make_packet(400, "중복임 ㄲㅈ")

    conn.cursor()

    return make_packet()