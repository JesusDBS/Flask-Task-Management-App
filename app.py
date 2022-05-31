from flask import Flask
from flask import make_response

app = Flask(__name__)

@app.route('/')
def index():
    response = make_response('<h1>Hello World Flask</h1>')
    return response

