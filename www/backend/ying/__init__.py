from flask import Flask
from flask_restful import Api
from .. import config
from ..instance.config import db

app = Flask(__name__)
app.config.from_object(config)
api = Api(app)

