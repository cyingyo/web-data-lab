import random
import re
import string
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders import Spider
from movies_spider.items import DoubanMoviesItem


class ReviewSpider(Spider):
    def parse(self, response):
        pass

    name = 'douban'
    custom_settings = {
        'ITEM_PIPELINES': {
            'movies_spider.pipelines.DoubanSpiderPipeline': 300
        }
    }

    def generate_cookie(self):
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
        return {'bid': bid}

    def start_requests(self):
        url_format = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10' \
                     '&tags=&start={0}&year_range={1},{1}'

        for y in range(2000, 2019):
            for s in range(0, 20, 20):
                # 豆瓣使用bid作为反爬策略，生成随机字符串即可应对，否则会封ip
                cookies = self.generate_cookie()
                url = url_format.format(s, y)
                yield scrapy.Request(url=url, callback=self.parse_list, cookies=cookies, meta={'year': y})

    def parse_list(self, response):
        desc_format = 'https://movie.douban.com/subject/{0}/'
        year = response.meta.get('year')
        _json_ = json.loads(response.body_as_unicode())
        _json_list = _json_['data']
        for _j in _json_list:
            _item = DoubanMoviesItem()
            _item['id'] = _j['id']
            _item['title'] = _j['title']
            _item['rate'] = _j['rate']
            _item['cover'] = _j['cover']
            _item['directors'] = _j['directors']
            _item['casts'] = _j['casts']
            _item['url'] = _j['url']
            _item['year'] = year
            desc_url = desc_format.format(_j['id'])
            cookies = self.generate_cookie()
            yield scrapy.Request(url=desc_url, callback=self.parse_desc, cookies=cookies, meta={'item': _item})

    def parse_desc(self, response):
        comment_format = 'https://movie.douban.com/subject/{0}/comments?start=0&limit=20&sort=new_score&status=P'
        rmhtml = re.compile(r'<[^>]+>', re.S)
        _item = response.meta.get('item')

        soup = BeautifulSoup(response.text, features='html.parser')
        html_content = str(soup.select_one('#link-report > span:nth-child(1)').text)
        html_content = html_content.strip()
        html_content = rmhtml.sub('', html_content)

        _item['description'] = html_content
        _item['comments'] = []

        comment_url = comment_format.format(_item['id'])
        cookies = self.generate_cookie()
        yield scrapy.Request(url=comment_url, callback=self.parse_comment, cookies=cookies, meta={'item': _item})

    def parse_comment(self, response):
        _item = response.meta.get('item')

        ans = _item['comments']
        soup = BeautifulSoup(response.text, features='html.parser')
        comments = soup.select('.comment-item')
        for comment in comments:
            _user = comment.select_one('div.comment > h3 > span.comment-info > a').text
            # 看没看过
            _type = comment.select_one('div.comment > h3 > span.comment-info > span:nth-child(2)').text
            try:
                _rate = comment.select_one('div.comment > h3 > span.comment-info > span.rating').attrs['title']
            except AttributeError:
                _rate = '未评分'
            _time = comment.select_one('div.comment > h3 > span.comment-info > span.comment-time').attrs['title']
            _content = comment.select_one('div.comment > p > span.short').text
            one = {
                'user': _user,
                'type': _type,
                'rate': _rate,
                'time': _time,
                'description': _content.replace("\n", "")
            }
            ans.append(one)
        yield _item
