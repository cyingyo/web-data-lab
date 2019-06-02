from flask import Flask, render_template
from flask_restful import Api
from .. import config


app = Flask(__name__, static_folder='assets', static_url_path='', template_folder='templates')
app.config.from_object(config)
api = Api(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/login')
def login():
    return app.send_static_file('html/login.html')


@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('html/index.html')


@app.route('/movie/<name>')
def movie(name):
    return app.send_static_file('html/movie.html')


@app.route('/search/<key>')
def search(key):
    return app.send_static_file('html/search.html')
