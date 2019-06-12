from flask_restful import Resource
from .. import db
douban = db['douban']
maoyan = db['maoyan']


class ListMovieApi(Resource):
    def get(self, page):
        
        pass

    def post(self, page):

        pass


class OneMovieApi:
    def get(self, title):
        pass


class SearchMovieApi:
    def get(self, keyword):
        pass
