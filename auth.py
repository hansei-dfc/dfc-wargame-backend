import jwt
import bcrypt
from flask import request
from flask_restx import Resource, Api, Namespace, fields

from auth.db.email_verify import send_verify_email
from auth.db.users import create_user, is_user_exists_email
from regex import verify_email, verify_password

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

        if (len(name) < 2 or not verify_email(email) or not verify_password(password)):
            return {
                "message": "Wrong email or password or name"
            }, 500
        elif name in users or is_user_exists_email(email):
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
