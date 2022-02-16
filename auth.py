import jwt
import bcrypt
from flask import request
from flask_restx import Resource, Api, Namespace, fields

from db import is_user_exists, is_verified, send_verify_email, create_user
import re

# Email regex
email_regex = re.compile(
    "^([\w\.\_\-])*[a-zA-Z0-9]+([\w\.\_\-])*([a-zA-Z0-9])+([\w\.\_\-])+@([a-zA-Z0-9]+\.)+[a-zA-Z0-9]{2,8}$")
# 비밀번호 8자 하나의 문자 하나의 숫자
password_regex = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

users = {}

Auth = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

user_fields = Auth.model('User', {  # Model 객체 생성
    'name': fields.String(description='a User Name', required=True, example="minpeter")
})

user_fields_auth = Auth.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required=True, example="password")
})

jwt_fields = Auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})


@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={500: 'Register Failed'})
    def post(self):
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        if (len(name) < 2 or not email_regex.match(email) or not password_regex.match(password)):
            return {
                "message": "Wrong email or password or name"
            }, 500
        elif name in users or is_verified(email, True) != None:
            return {
                "message": "name or email already exists"
            }, 500
        else:
            id = create_user(name, email, password)
            if (send_verify_email(id, email)):
                users[name] = bcrypt.hashpw(password.encode(
                    "utf-8"), bcrypt.gensalt())  # 비밀번호 저장
                return {
                    # str으로 반환하여 return
                    "message": "Success",
                    'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256").decode('utf8')
                }, 200
            else:
                return {
                    "message": "Email sending failed"
                }, 500


@Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'User Not Found'})
    @Auth.doc(responses={500: 'Auth Failed'})
    def post(self):
        name = request.json['name']
        password = request.json['password']
        if name not in users:
            return {
                "message": "User Not Found"
            }, 404
        # 비밀번호 일치 확인
        elif not bcrypt.checkpw(password.encode('utf-8'), users[name]):
            return {
                "message": "Auth Failed"
            }, 500
        else:
            return {
                # str으로 반환하여 return
                'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256").decode('utf8')
            }, 200


@Auth.route('/get')
class AuthGet(Resource):
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'Login Failed'})
    def get(self):
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {"message": "Please Login"}, 404
        data = jwt.decode(header, "secret", algorithms="HS256")
        return data, 200
