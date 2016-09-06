import json

from flask import Flask

app = Flask(__name__)
from . import views

with open('secrets.json', 'r') as file:
    secrets = json.load(file)

app.secret_key = secrets.get('flask_secret')
