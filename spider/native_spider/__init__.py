from pymongo import MongoClient

__username__ = 'cying'
__password__ = 'Hk8Thdtnct'
__host__ = '39.106.55.9:27017'
__mongo_url__ = 'mongodb://{}:{}@{}'.format(__username__, __password__, __host__)

__mg__ = MongoClient(__mongo_url__)
db = __mg__['webdata']
