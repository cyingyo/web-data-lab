from spider.native_spider import db

maoyan = db['maoyan']
douban = db['douban']
unimovies = db['unimovies']


def mix_douban():
    douban_data = douban.find()
    for db_row in douban_data:
        title = db_row['title']
        my_row = maoyan.find_one({'title': title})
        try:
            if my_row is not None:
                comments = []
                comments.extend(db_row['comments'])
                comments.extend(my_row['comments'])
                mixed = {
                    'id': db_row['id'],
                    'title': db_row['title'],
                    'origin_title': my_row['origin_title'],
                    'db_rate': db_row['rate'],
                    'my_rate': my_row['rate'],
                    'my_rate_base': my_row['rate_base'],
                    'piaofang': my_row['piaofang'],
                    'cover': my_row['cover'],
                    'directors': db_row['directors'],
                    'casts': db_row['casts'],
                    'db_url': db_row['url'],
                    'my_url': my_row['url'],
                    'comments': comments,
                    'description': db_row['description'],
                    'year': my_row['year'],
                    'type': my_row['type'],
                    'time': my_row['time'],
                    'douban': True,
                    'maoyan': True
                }
                maoyan.update_one({'title': title}, {'$set': {'inDouban': True}})
                unimovies.insert_one(mixed)
                print('{} 已Mixed！'.format(title))
            else:
                mixed = {
                    'id': db_row['id'],
                    'title': db_row['title'],
                    'db_rate': db_row['rate'],
                    'cover': db_row['cover'],
                    'directors': db_row['directors'],
                    'casts': db_row['casts'],
                    'db_url': db_row['url'],
                    'comments': db_row['comments'],
                    'description': db_row['description'],
                    'year': db_row['year'],
                    'douban': True,
                    'maoyan': False
                }
                unimovies.insert_one(mixed)
                print('{} 已插入！'.format(title))
        except Exception as e:
            print('{} 出现错误 {}'.format(title, e))


def insert_maoyan():
    mys = maoyan.find({'inDouban': {'$exists': False}})
    base_id = 100000000
    count = 0
    for my_row in mys:
        _id = str(base_id + count)
        count += 1
        mixed = {
            'id': _id,
            'title': my_row['title'],
            'origin_title': my_row['origin_title'],
            'my_rate': my_row['rate'],
            'my_rate_base': my_row['rate_base'],
            'piaofang': my_row['piaofang'],
            'cover': my_row['cover'],
            'directors': my_row['directors'],
            'casts': my_row['casts'],
            'my_url': my_row['url'],
            'comments': my_row['comments'],
            'description': my_row['description'],
            'year': my_row['year'],
            'type': my_row['type'],
            'time': my_row['time'],
            'douban': False,
            'maoyan': True
        }
        unimovies.insert_one(mixed)
        print('{} 已插入'.format(my_row['title']))


if __name__ == '__main__':
    mix_douban()
    insert_maoyan()
