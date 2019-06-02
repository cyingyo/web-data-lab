import os
import xml.dom.minidom as xmldom
import requests
import random
import re
import time
from spider.native_spider import db
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont


class Maoyan:
    def __init__(self):
        """
        yearId：猫眼电影
            2000-2010：5
            2001：6
            2002：7
            ......
            2019：14
        offset：分页，每页30条数据
        """
        self.list_tmp = 'https://maoyan.com/films?showType=3&sortId=1&yearId={0}&offset={1}'
        self.movie_tmp = 'https://maoyan.com/films/{}'
        self.db = db['maoyan']

    def header(self):
        header = {
            'Accept': '*/*;',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'maoyan.com',
            'Referer': 'http://maoyan.com/',
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

    # 13：270，电影 假面骑士亚马逊们剧场版 最后的审判 仮面ライダーアマゾンズ THE MOVIE 最後ノ審判 已爬取！
    # downloading //vfile.meituan.net/colorstone/3b621bd557d47be6b58c81d427efc2f32080.woff
    # 13：270，电影 紫罗兰永恒花园 已爬取！
    # downloading //vfile.meituan.net/colorstone/3b621bd557d47be6b58c81d427efc2f32080.woff
    def start_crawling(self, start, end, limit=500):
        for y in range(start, end+1):
            for s in range(0, limit, 30):
                list_url = self.list_tmp.format(y, s)
                content = requests.get(list_url, headers=self.header())
                # 使用正则表达式将所有的电影id提取出来
                ids = re.findall(re.compile("{movieId:(.*)}"), content.text)
                for _id in ids:
                    # 解析每一页的数据
                    movie_url = self.movie_tmp.format(_id)
                    try:
                        _m_data = self.parse_movie(movie_url)
                        # 存储到相应的数据库中，这里采用mongodb
                        self.store_data(_m_data)
                        print('{}：{}，电影 {} 已爬取！'.format(y, s, _m_data['title']))
                        # 不要太流氓
                        time.sleep(random.random() * 5)
                    except Exception as e:
                        print('爬取出现错误，可能被封ip了. {}'.format(e))
        # movie_url = 'https://maoyan.com/films/1218727'
        # _m_data = self.parse_movie(movie_url)
        # # 存储到相应的数据库中，这里采用mongodb
        # self.store_data(_m_data)
        # print('电影 {} 已爬取！'.format(_m_data['title']))
        # print('爬取完成！')

    def parse_movie(self, url):
        html_content = requests.get(url, headers=self.header()).text

        p = re.compile(r"url\('(.*?)'\) format\('woff'\);")
        # woff 文件的地址，每次请求都是不一样的，每次都要下载并处理
        _woff_url = re.findall(p, html_content)[0]
        font_dict = self.handle_fonts(_woff_url)
        html_content = self.parse_font(html_content, font_dict)
        bs = BeautifulSoup(html_content, 'lxml')

        # maoyan id
        _id = url.split('/')[-1]
        # 电影名
        _title = bs.select_one('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > h3').get_text()
        # 电影英文名（外文名）
        _for_title = bs.select_one('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > div').get_text()
        # 封面url
        _cover = bs.select_one('body > div.banner > div > div.celeInfo-left > div > img')['src']
        # 导演们
        _directors = bs.select('#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(2) > div.mod-content > div > div:nth-child(1) > ul > li > div > a')
        # 演员们
        _casts = bs.select('#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(2) > div.mod-content > div > div:nth-child(2) > ul > li > div > a')
        # 类型
        _type = bs.select_one('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > ul > li:nth-child(1)').get_text()
        # 制片方/时长
        _time = bs.select_one('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > ul > li:nth-child(2)').get_text()
        # 何年上映
        _year = bs.select_one('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > ul > li:nth-child(3)').get_text()
        # 影片简介
        _desc = bs.select_one('#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(1) > div.mod-content > span').get_text()

        # 影片评论
        _cmts = []
        try:
            _raw_cmts = bs.select('#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(5) > div.mod-content > div > ul > li')
            for _cmt in _raw_cmts:
                _one = {
                    'user': _cmt.select_one('div.main > div.main-header.clearfix > div.user > span.name').get_text(),
                    'rate': _cmt.select_one('div.main > div.main-header.clearfix > div.time > ul')['data-score'],
                    'time': _cmt.select_one('div.main > div.main-header.clearfix > div.time')['title'],
                    'content': _cmt.select_one('div.main > div.comment-content').get_text()
                }
                _cmt_type = _cmt.select_one('div.main > div.main-header.clearfix > div.user > span.tag')
                try:
                    _one['type'] = _cmt_type.get_text()
                except:
                    _one['type'] = '未购'
                _cmts.append(_one)
        except Exception as e:
            print('获取评论时出现错误！可能由于该电影暂无评论信息{}'.format(e))

        # 评分人数
        try:
            _people_num = bs.select_one('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-stats-container > div:nth-child(1) > div > div > span > span').get_text()
        except:
            _people_num = '无人评分'

        # 评分
        try:
            _rate = bs.select_one('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-stats-container > div:nth-child(1) > div > span > span').get_text()
        except:
            _rate = '暂无评分'

        # 票房
        try:
            _piaofang = bs.select_one('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-stats-container > div:nth-child(2) > div > span.stonefont').get_text()
            try:
                _piaofang += bs.select_one('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-stats-container > div:nth-child(2) > div > span.unit').get_text()
            except:
                pass
        except:
            _piaofang = '暂无票房'

        movie = {
            'id': _id,
            'title': _title,
            'origin_title': _for_title,
            'rate': _rate,
            'rate_base': _people_num,
            'piaofang': _piaofang,
            'cover': _cover,
            'directors': [str(x.get_text()) for x in _directors],
            'casts': [str(x.get_text()) for x in _casts],
            'url': url,
            'comments': _cmts,
            'description': _desc,
            'year': _year,
            'type': _type,
            'time': _time
        }
        return movie

    def store_data(self, _data):
        self.db.insert_one(_data)

    def handle_fonts(self, url):
        print('downloading {}'.format(url))
        r = requests.get('http:' + url)
        with open("./static/damn.woff", "wb") as code:
            code.write(r.content)
        font = TTFont("./static/damn.woff")
        font.saveXML('./static/damnTo.xml')

        # 加载字体模板
        num = [8, 6, 2, 1, 4, 3, 0, 9, 5, 7]
        data = []
        new_font = []
        _xml_file_path = os.path.abspath("./static/temp.xml")
        _dom = xmldom.parse(_xml_file_path)
        _ele = _dom.documentElement
        # 标签中是这些数字的具体坐标画法，一个TTGlyph对应一个数字
        # 其中contour标签的坐标数据，就是唯一确定数字的方法
        _TTGlyphs = _ele.getElementsByTagName("TTGlyph")
        for i in range(len(_TTGlyphs)):
            th = _TTGlyphs[i].toprettyxml()
            _pattern = re.compile(r"name=\"(.*)\"")
            _found = _pattern.findall(str(th))
            data.append(str(th).replace(_found[0], '').replace("\n", ''))

        # 根据字体模板解码本次请求下载的字体
        _down_xml = os.path.abspath("./static/damnTo.xml")
        _new_dom = xmldom.parse(_down_xml)
        _new_ele = _new_dom.documentElement
        _new_TTGlyphs = _new_ele.getElementsByTagName("TTGlyph")
        for i in range(len(_new_TTGlyphs)):
            th = _new_TTGlyphs[i].toprettyxml()
            _pattern = re.compile(r"name=\"(.*)\"")
            _found = _pattern.findall(th)
            get_code = th.replace(_found[0], '').replace("\n", '')
            for j in range(len(data)):
                if get_code == data[j]:
                    new_font.append(num[j])

        ans = {}
        font = TTFont("./static/damn.woff")
        font_list = font.getGlyphNames()
        font_list.remove('glyph00000')
        font_list.remove('x')
        for i in range(len(font_list)):
            font_list[i] = str(font_list[i]).lower().replace("uni", '&#x') + ';'
            ans[font_list[i]] = new_font[i]

        return ans

    def parse_font(self, ori, font_dict):
        for uni, num in font_dict.items():
            if uni in ori:
                ori = ori.replace(uni, str(num))
        return ori


if __name__ == '__main__':
    spider = Maoyan()
    spider.start_crawling(14, 14)
    # 1201982
