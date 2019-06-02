import re
import string
import random
import requests
import time
from bs4 import BeautifulSoup
from spider.native_spider import db

table = db['douban']

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}
]
# proxys = []
# with open('./proxy.txt', 'r') as rf:
#     proxys.extend(rf.readlines())


# 大约 20*1000*11 + 1000 = 22w次请求
# def generate_proxy():
#     proxy = random.choice(proxys)
#     return {'https': proxy}
hasCookies = False
cookies = {}


def generate_cookie():
    global cookies

    if not hasCookies:
        url = 'https://www.douban.com'
        r = requests.get(url)
        cookies = r.cookies
    bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
    cookies['bid'] = bid


def extract_comments_from_html(_html):
    ans = []
    soup = BeautifulSoup(_html, features='html.parser')
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
            'content': _content.replace("\n", "")
        }
        ans.append(one)
    return ans


def get_movie_comments(_id):
    global hasCookies

    url_format = 'https://movie.douban.com/subject/{0}/comments?start=0&limit=20&sort=new_score&status=P'
    # 豆瓣网站的评论只提供220条，再往后都无法显示。每页固定20个，更改limit参数也没用。
    comments = []

    url = url_format.format(_id)
    generate_cookie()
    # _proxy = generate_proxy()
    try:
        html_content = requests.get(url, headers=headers[random.randint(0, len(headers)-1)], cookies=cookies).text
        ret_ans = extract_comments_from_html(html_content)
        comments.extend(ret_ans)
    except Exception as e:
        print('获取Comment失败！-> {}'.format(e))
        hasCookies = False
    time.sleep(1.7 + random.random() * 1.3)
    return comments


def get_movie_description(_id):
    desc_format = 'https://movie.douban.com/subject/{0}/'
    url = desc_format.format(_id)
    generate_cookie()
    desc = '影片无简介'

    try:
        html_content = requests.get(url, headers=headers[random.randint(0, len(headers)-1)], cookies=cookies).text
        soup = BeautifulSoup(html_content, features='html.parser')
        rmhtml = re.compile(r'<[^>]+>', re.S)
        desc = str(soup.select_one('#link-report > span:nth-child(1)').text).strip()
        desc = rmhtml.sub('', desc)
    except Exception as e:
        print('获取Description失败！-> {}'.format(e))
    time.sleep(1.7 + random.random() * 1.3)
    return desc


def get_movies_list():
    global hasCookies

    # json API 接口，指定年限的所有地区的所有电影，按照标记人数降序排序
    url_format = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={0}&year_range={1},{1}'

    count = 1
    for y in range(2019, 2020):
        for s in range(0, 500, 20):
            # 豆瓣使用bid作为反爬策略，生成随机字符串即可应对，否则会封ip
            generate_cookie()
            url = url_format.format(s, y)
            try:
                # 访问接口，获取json数据
                json_data = requests.get(url, headers=headers[random.randint(0, len(headers)-1)], cookies=cookies).json()
                for _j in json_data['data']:
                    movie = {
                        'id': _j['id'],
                        'title': _j['title'],
                        'rate': _j['rate'],
                        'cover': _j['cover'],
                        'directors': _j['directors'],
                        'casts': _j['casts'],
                        'url': _j['url'],
                        'comments': get_movie_comments(_j['id']),
                        'description': get_movie_description(_j['id']),
                        'year': y
                    }
                    table.insert_one(movie)
                    print('{}，{} - 成功获取{}的信息及评论！'.format(count, y, _j['title']))
                    count += 1
                time.sleep(1.7 + random.random() * 1.3)
            except Exception as e:
                hasCookies = False
                print('获取List失败！-> {}'.format(e))
        time.sleep(60 + random.random() * 60)
    print('爬取2000-2018年电影完成，共爬取{}'.format(count))


if __name__ == '__main__':
    get_movies_list()
