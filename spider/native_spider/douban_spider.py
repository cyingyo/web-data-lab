import re
import string
import random
import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

__username__ = 'cying'
__password__ = 'Hk8Thdtnct'
__host__ = '39.106.55.9:27017'
__mongo_url__ = 'mongodb://{}:{}@{}'.format(__username__, __password__, __host__)

__mg__ = MongoClient(__mongo_url__)
db = __mg__['webdata']


class Douban:
    def __init__(self):
        self.list_tmp = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={0}&year_range={1},{1}'
        self.movie_tmp = 'https://movie.douban.com/subject/{0}/'
        self.has_cookies = False
        self.db = db['douban_f']

    def header(self):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Connection': 'keep-alive',
            'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'movie.douban.com'
        }
        uas = [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'
        ]
        header['User-Agent'] = random.choice(uas)
        return header

    def cookie(self):
        cookies = {}
        if not self.has_cookies:
            url = 'https://www.douban.com'
            r = requests.get(url)
            cookies = r.cookies
        # 豆瓣使用bid作为反爬策略，生成随机字符串即可应对，否则会封ip
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
        cookies['bid'] = bid
        return cookies

    def start_crawling(self, s, e, limit=500):
        for y in range(s, e+1):
            for s in range(0, limit, 20):
                url = self.list_tmp.format(s, y)
                try:
                    # 访问接口，获取json数据
                    json_data = requests.get(url, headers=self.header(), cookies=self.cookie()).json()
                    for _j in json_data['data']:
                        movie = {
                            'id': _j['id'],
                            'title': _j['title'],
                            'rate': _j['rate'],
                            'cover': _j['cover'],
                            'directors': _j['directors'],
                            'casts': _j['casts'],
                            'url': _j['url'],
                            'year': y
                        }
                        movie_url = self.movie_tmp.format(_j['id'])
                        # 从页面中获取更详细的信息
                        self.parse_movie(movie_url, movie)
                        self.store_data(movie)
                        # 不要太流氓
                        time.sleep(2 + random.random() * 1.3)
                        print('{}，{} - 成功获取 {} 的信息及评论！'.format(y, s, _j['title']))
                except Exception as e:
                    self.has_cookies = False
                    print('获取List失败！-> {} -> {}'.format(e, url))
            # 每次爬完一年的数据，等一会再爬，会封 ip
            time.sleep(600 + random.random() * 600)
        print('爬取{}-{}年电影完成'.format(s, e))

    def parse_movie(self, url, movie):
        try:
            html_content = requests.get(url, headers=self.header(), cookies=self.cookie()).text
            soup = BeautifulSoup(html_content, features='lxml')

            # 影片简介
            try:
                _desc = str(soup.select_one('#link-report > span:nth-child(1)').get_text()).strip()
            except:
                _desc = '影片无简介'

            # 评论
            _cmts = []
            ori_comments = soup.select('#hot-comments > div.comment-item')
            for comment in ori_comments:
                # 用户名
                _user = comment.select_one('div.comment > h3 > span.comment-info > a').get_text()
                # 看没看过
                _type = comment.select_one('div.comment > h3 > span.comment-info > span:nth-child(2)').get_text()
                # 评分
                try:
                    _rate = comment.select_one('div.comment > h3 > span.comment-info > span.rating').attrs['title']
                except AttributeError:
                    _rate = '未评分'
                # 评价时间
                _time = comment.select_one('div.comment > h3 > span.comment-info > span.comment-time').attrs['title']
                # 评论信息，先获取被折叠的全评论，如果太短，直接用short
                try:
                    _content = comment.select_one('div.comment > p > span.full').get_text()
                except:
                    _content = comment.select_one('div.comment > p > span.short').get_text()

                one = {
                    'user': _user,
                    'type': _type,
                    'rate': _rate,
                    'time': _time,
                    'content': _content.replace("\n", "")
                }
                _cmts.append(one)

            movie['description'] = _desc
            movie['comments'] = _cmts
        except Exception as e:
            self.has_cookies = False
            print('获取电影 {} 详细信息失败！-> {}'.format(movie['title'], e))

    def store_data(self, movie):
        self.db.insert_one(movie)


if __name__ == '__main__':
    spider = Douban()
    spider.start_crawling(2000, 2019)
    # get_movies_list()
