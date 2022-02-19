from dotenv import load_dotenv
load_dotenv()

from auth import Auth
from flask_restx import Api
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources={r'*': {'origins': '*'}})

api = Api(
    app,
    version='0.1',
    title="hansei ctf",
    description="hansei ctf",
    terms_url="/",
    contact="kali2005611@gmail.com",
    license="MIT"
)

api.add_namespace(Auth, '/auth')


@app.route('/')
def home():
    return jsonify({"massage": 'This api is the api that creates the sandbox of hansei wargame.'})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
