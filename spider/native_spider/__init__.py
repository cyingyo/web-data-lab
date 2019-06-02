from pymongo import MongoClient

__username__ = 'cying'
__password__ = 'cying'
__host__ = '127.0.0.1:123456'
__mongo_url__ = 'mongodb://{}:{}@{}'.format(__username__, __password__, __host__)

__mg__ = MongoClient(__mongo_url__)
db = __mg__['webdata']
