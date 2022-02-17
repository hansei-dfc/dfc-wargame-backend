from datetime import datetime
from pkgutil import extend_path
from urllib.parse import urljoin
import jwt
from flask import redirect, request
from flask_restx import Resource, Namespace, fields

from db import check_password, check_verify_code, get_user_id, is_verified, create_user, transform_verified_user
import re
import env
from email_verify import parse_verify_data, send_verify_email

# Email regex
email_regex = re.compile('(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])')
# 최소 8자, 대문자 1개 이상, 소문자 1개, 숫자 1개
password_regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")

Auth = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

user_fields_auth = Auth.model('User login', {  # Model 객체 생성
    'email': fields.String(description='user email', required=True, example="qlskssk@gmail.com"),
    'password': fields.String(description='Password', required=True, example="Password1")
})


user_fields_register = Auth.inherit('User register', user_fields_auth, {
    'name': fields.String(description='user name', required=True, example="wa sans"),
    'redirect_url': fields.String(description='email verify redirect url', required=False, example="http://localhost/")
})

jwt_fields = Auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})


@ Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_register)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={400: 'Bad request'})
    @Auth.doc(responses={403: 'Email already exists'})
    @Auth.doc(responses={500: 'Register Failed'})
    def post(self):
        try:
            name = request.json['name']
            email = request.json['email']
            password = request.json['password']
            redirect_url = request.json.get('redirect_url', '')
        except:
            return {
                "message": "Bad request"
            }, 400

        # 이메일, 비밀번호 테스트
        name_len = len(name)
        if (name_len < 2 or name_len > 50 or not email_regex.match(email) or not password_regex.match(password)):
            return {
                "message": "Wrong email or password or name"
            }, 400

        # 유저가 이미 있는지
        if is_verified(email, True) != None:
            return {
                # 닉네임 중복 가능해요
                "message": "email already exists"
            }, 403

        # 임시 유저 추가
        temp_id, verify_code = create_user(name, email, password, True)
        # 처리 오류
        if temp_id == None:
            return {
                "message": "Internal error"
            }, 500

        # 인증 메일 발송
        if send_verify_email(temp_id, email, verify_code, redirect_url):
            return {
                "message": "Success"
            }, 200
        else:
            return {
                "message": "Email sending failed"
            }, 500


@ Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={400: 'Bad request'})
    @Auth.doc(responses={403: 'Email not verified'})
    @Auth.doc(responses={404: 'Auth Failed'})
    def post(self):
        try:
            email = request.json['email']
            password = request.json['password']
        except:
            return {"message": "Bad request"}, 400

        # 올바른 이메일인지
        if not email_regex.match(email):
            return {"message": "Auth failed"}, 404

        # 이메일 인증됬는지
        if is_verified(email, True) == False:
            return {"message": "Email not verified"}, 403

        # 비밀번호 일치 확인
        if check_password(email, True, password) != True:
            return {"message": "Auth failed"}, 404

        # 유저 id 가져옴, sql 처리속도 높이기 위함.
        user_id = get_user_id(email, False)

        # 킹론상 가능함
        if user_id == None:
            return {"message": "Internal error"}, 500

        return {
            "message": "Success",
            "Authorization": jwt.encode({
                'id': user_id,
                'email': email,
                'exp': datetime.utcnow() + env.jwt_exp_period
            }, env.jwt_secret, algorithm="HS256")
        }, 200


@Auth.route('/email_verify')
class EmailVerify(Resource):
    @Auth.doc(responses={301: 'Bad request or Invalid code'})
    @Auth.doc(responses={302: 'Success or Error'})
    def get(self):
        v_code = parse_verify_data(request.args.get("vc"))
        redirect_url = request.args.get("r", "")
        if not redirect_url or redirect_url.isspace(
        ):
            redirect_url = env.default_email_verify_redirect_url

        # 인증코드가 없어!
        if v_code == None:
            return redirect(urljoin(redirect_url, "?status=none"), 301)

        user_id = v_code[0]
        vef_code = v_code[1]

        # 코드 검증
        if check_verify_code(user_id, vef_code) != True:
            return redirect(urljoin(redirect_url, "?status=invalid"), 301)

        # 처리 오류
        if transform_verified_user(user_id) == None:
            return redirect(urljoin(redirect_url, "?status=error"))

        # 리다이렉트
        return redirect(urljoin(redirect_url, "?status=success"))


@ Auth.route('/get')
class AuthGet(Resource):
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'Bad request or Invalid token'})
    @Auth.doc(responses={403: 'Token Expired'})
    def get(self):
        try:
            header = request.headers.get('Authorization', None)
            header = header[header.find('Bearer')+6:].strip()
            data = jwt.decode(header, env.jwt_secret, algorithms="HS256")
            return data, 200
        except jwt.ExpiredSignatureError:
            return {"message": "Token Expired"}, 403
        except:
            return {"message": "Bad request"}, 404
