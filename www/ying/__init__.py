from flask import Flask
from flask_restful import Api
from .. import config


app = Flask(__name__, static_folder='assets', template_folder='templates')
app.config.from_object(config)
api = Api(app)
