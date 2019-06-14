from flask import Flask
from flask_restful import Api
from datetime import timedelta
from www import config
from .controller.movie import ListMovieApi, OneMovieApi, SearchMovieApi

app = Flask(__name__, static_folder='assets', static_url_path='')
app.config.from_object(config)
app.config['JSON_AS_ASCII'] = False
# 配置缓存最大时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
# 配置session有效期
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=1)
api = Api(app)

api.add_resource(ListMovieApi, '/api/movie/list/<int:page>')
api.add_resource(SearchMovieApi, '/api/movie/search/<int:page>')
api.add_resource(OneMovieApi, '/api/movie/<int:_id>')


@app.route('/')
@app.route('/index')
def root():
    return app.send_static_file('html/index.html')


@app.route('/movie/<string:_id>')
def movie(_id):
    return app.send_static_file('html/movie.html')


@app.route('/search/<string:key>')
def searching(key):
    return app.send_static_file('html/search.html')

