from flask_restful import Resource, reqparse
from ...instance.config import db
from ..output import Output
import pymongo
unimovies = db['unimovies']


class ListMovieApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('location', type=str, location='json')
        self.reqparse.add_argument('year', type=str, location='json')
        self.reqparse.add_argument('type', type=str, location='json')
        self.reqparse.add_argument('rate', type=str, location='json')
        self.page_size = 24
        super(ListMovieApi, self).__init__()

    def is_not_empty(self, arg):
        if arg is None or arg == '':
            return False
        else:
            return True

    def post(self, page):
        print('list')
        skip_num = (page - 1) * self.page_size

        args = self.reqparse.parse_args()
        _location = args['location']
        _year = args['year']
        _type = args['type']
        _rate = args['rate']

        search_args = {}
        project_args = {'id': 1, 'title': 1, 'cover': 1, 'maoyan': 1, 'douban': 1, '_id': 0}
        if self.is_not_empty(_location):
            search_args['time'] = {'$regex': '.*{}.*'.format(_location)}
        if self.is_not_empty(_year):
            search_args['year'] = {'$regex': '.*{}.*'.format(_year)}
        if self.is_not_empty(_type):
            search_args['type'] = {'$regex': '.*{}.*'.format(_type)}
        if self.is_not_empty(_rate):
            search_args['$or'] = [
                {'db_rate': {'$regex': '^{}.*'.format(_rate)}},
                {'my_rate': {'$regex': '^{}.*'.format(_rate)}}
            ]

        result = unimovies.find(search_args, project_args)\
            .sort([('year', pymongo.DESCENDING), ('my_rate', pymongo.DESCENDING)])\
            .skip(skip_num).limit(self.page_size)

        result = list(result)
        ans = {
            'movies': list(result),
            'last': len(result) == 0
        }
        return Output.success(ans)


class OneMovieApi(Resource):
    def __init__(self):
        super(OneMovieApi, self).__init__()

    def get(self, _id):
        project_args = {'_id': 0}

        result = unimovies.find_one({'id': str(_id)}, project_args)
        if result is None:
            return Output.error()
        return Output.success(result)


class SearchMovieApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('keyword', type=str, location='json')
        self.page_size = 24
        super(SearchMovieApi, self).__init__()

    def post(self, page):
        args = self.reqparse.parse_args()
        keyword = args['keyword']
        keyword = keyword.encode('utf8').decode('utf8')

        print(type(keyword))
        print('input key : {}'.format(keyword))
        skip_num = (page - 1) * self.page_size

        search_args = {'title': {'$regex': '.*{}.*'.format(keyword)}}
        print('search args : {}'.format(search_args))
        project_args = {'id': 1, 'title': 1, 'cover': 1, 'maoyan': 1, 'douban': 1, '_id': 0}

        result = unimovies.find(search_args, project_args)\
            .sort([('year', pymongo.DESCENDING), ('my_rate', pymongo.DESCENDING)])\
            .skip(skip_num).limit(self.page_size)
        result = list(result)

        ans = {
            'movies': list(result),
            'last': len(result) == 0
        }
        return Output.success(ans)
