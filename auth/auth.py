from flask import Blueprint
from auth.signup import signup

auth = Blueprint('auth', __name__)

auth.register_blueprint(signup)

@auth.route('/auth')
def index():
    return "auth"