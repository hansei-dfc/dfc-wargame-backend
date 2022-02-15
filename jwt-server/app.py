from flask import Flask
from flask_restx import Resource, Api
from auth import Auth

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title="Minpeter's API Server",
    description="Minpeter's sandbox API Server!",
    terms_url="/",
    contact="kali2005611@gmail.com",
    license="MIT"
)

api.add_namespace(Auth, '/auth')

if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=5000)
