from dotenv import load_dotenv

from auth.db.email_verify import check_verify_code, db_create_verify, is_verified
from auth.db.users import create_user
load_dotenv()

from flask import Flask
from auth.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

@app.route('/')
def board():
    return "index"

app.run(host="0.0.0.0", port=5001, debug=True)