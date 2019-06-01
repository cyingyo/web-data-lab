from pymongo import MongoClient

__username__ = 'admin'
__password__ = 'admin'
__host__ = '127.0.0.1:12345'
__mongo_url__ = 'mongodb://{}:{}@{}'.format(__username__, __password__, __host__)

__mg__ = MongoClient(__mongo_url__)
db = __mg__['webdata']
