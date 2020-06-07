#coding: utf-8
import re
import time
import random
import requests
from crawler.config import rent_type, city_info, proxypool_url, user_agent_list,headers, cities
from crawler.db_handler import db
from crawler.my_logger import logger
from crawler.config import table_name, table_url
from crawler.my_mail import mail


class Rent():
    """
    初始化函数，获取租房类型（整租、合租）、要爬取的城市分区信息以及连接mongodb数据库
    """
    def __init__(self, db):
        self.rent_type = rent_type
        self.city_info = city_info
        self.db = db

    @staticmethod
    def get_random_proxy(proxypool_url):
        """
        get random proxy from proxypool
        :param proxypool_url:目标url一个字符串
        :return: proxy
        """
        proxy = requests.get(proxypool_url).text.strip()
        proxies = {
                   'http': 'https://' + proxy}
        return proxies

    @staticmethod
    def get_url(index, city):
        '''
        用于爬虫过程中随机访问其他页面
        :param index: 一个随机整数
        :param city: 城市代号，在cities中
        :return:
        '''

        if city == None:
            return
        # 城市值为None时，我们就跳出
        else:
            if index == 1 or index == 0:
                url = 'https://m.lianjia.com/{city}/'.format(city=city)
                return url
            if 1 < index < 3:
                url = 'https://m.lianjia.com/chuzu/{city}/'.format(city=city)
                return url
            if 3 <= index < 7:
                url = 'https://m.lianjia.com/{city}/ershoufang/index/'.format(city=city)
                return url
            if 7 <= index < 10:
                url = 'https://m.lianjia.com/chuzu/{city}/zufang/rt200600000'.format(city=city)
                return url
            if 10 <= index < 13:
                url = 'https://m.lianjia.com/chuzu/{city}/zufang/rp0rmp1/'.format(city=city)
                return url
            if 13 <= index < 15:
                url = 'https://m.lianjia.com/{city}/loupan/fang/'.format(city=city)
                return url
            if 15 <= index < 18:
                url = 'https://m.lianjia.com/{city}/xiaoqu/'.format(city=city)
                return url
            else:
                url = 'https://m.lianjia.com/chuzu/{city}/zufang/'.format(city=city)
                return url

    @staticmethod
    def get_headers(headers,agent_list):
        '''

        :param headers:请求头
        :param agent_list: 浏览器标志列表
        :return:完整的请求头
        '''
        # headers = dict()
        user_agent = random.choice(agent_list)
        headers['User-Agent'] = user_agent
        return headers


    def get_is_inserted(self,index, table_name):
        '''
        查询table_name 中的字段index
        :param index: 数据库表中的unique字段
        :param table_name: 要查询的表
        :return:返回一个集合set
        '''
        is_inserted_data = self.db.get_column(index, table_name=table_name)
        return set(is_inserted_data)


    def get_data(self):
        """
        爬取不同租房类型、不同城市各区域的租房信息
        :return: None
        """
        count = 0                                           #每个代理IP爬取的次数
        house_counts = 0                                    #统计房源数量
        loop = 0
        for ty, type_code in self.rent_type.items():        # 整租、合租
            for city, info in self.city_info.items():       # 城市、城市各区的信息
                for dist, dist_py in info[2].items():       # 各区及其拼音
                    is_inserted_data = self.get_is_inserted('m_url', table_name=table_name)  # 已经在数据库中的数据
                    is_crawler_url = self.get_is_inserted('url', table_name=table_url)       # 已经爬过的URL
                    proxies = self.get_random_proxy(proxypool_url)                           # 代理IP
                    header = self.get_headers(headers=headers,agent_list=user_agent_list)    # 请求头
                    print(header)
                    timeout = random.choice(range(10,30))

                    res_bc = requests.get('https://m.lianjia.com/chuzu/{}/zufang/{}/'.format(info[1], dist_py),
                                      headers=headers,proxies=proxies,timeout=timeout)
                    count += 1
                    print(res_bc.status_code)
                    if count >= 3:
                        proxies = self.get_random_proxy(proxypool_url)  # 代理IP
                        header = self.get_headers(headers=headers, agent_list=user_agent_list)
                        index = random.choice(range(0, 20))
                        cy = random.choice(cities)
                        url = self.get_url(index, cy)
                        requests.get(url, headers=header, proxies=proxies, timeout=timeout)
                        time.sleep(random.uniform(1, 2.5))
                        count = 0

                    pa_bc = r"data-type=\"bizcircle\" data-key=\"(.*)\" class=\"oneline \">"
                    bc_list = re.findall(pa_bc, res_bc.text)
                    self._write_bc(bc_list)
                    bc_list = self._read_bc()  # 先爬取各区的商圈，最终以各区商圈来爬数据，如果按区爬，每区最多只能获得2000条数据
                    count = 0
                    if len(bc_list) > 0:
                        for bc_name in bc_list:
                            logger.info('开始爬取{}市{}-{}的{}的数据！'.format(city, dist, bc_name, ty))
                            print('开始爬取{}市{}-{}的{}的数据！'.format(city, dist, bc_name, ty))
                            totals = 0
                            idx = 0
                            has_more = 1
                            if house_counts / 5000 > loop:  # 每爬取5000套房源，发送一封邮件告知爬取到的数量
                                is_crawler_counts = self.db.get_counts()
                                msg_text = "成功爬取%d条, 已经爬取到%d条" % (house_counts, is_crawler_counts)
                                msg_subject = 'house_data_crawler'
                                mail(msg_text=msg_text, msg_subject=msg_subject)
                                loop += 1
                            while has_more:
                                if count >= 3:      #每个区每爬三次随机跳转到其他页面，并休眠一段时间
                                    proxies = self.get_random_proxy(proxypool_url)  # 代理IP
                                    header = self.get_headers(headers=headers, agent_list=user_agent_list)
                                    index = random.choice(range(0,20))
                                    cy = random.choice(cities)
                                    url = self.get_url(index, cy)
                                    requests.get(url, headers=header,proxies=proxies,timeout=timeout)
                                    time.sleep(random.uniform(0.5,1))
                                    count = 0

                                try:
                                    url = 'https://app.api.lianjia.com/Rentplat/v1/house/list?city_id={}&condition={}' \
                                          '/rt{}&limit=3000&offset={}&request_ts={}&scene=list'.format(info[0],
                                                                                                     bc_name,
                                                                                                     type_code,
                                                                                                     idx*3000,
                                                                                                     int(time.time()))
                                    store_url = 'https://app.api.lianjia.com/Rentplat/v1/house/list?city_id={}&condition={}' \
                                          '/rt{}&limit=3000&offset={}'.format(info[0],
                                                                             bc_name,
                                                                             type_code,
                                                                             idx*3000
                                                                             )
                                    if store_url in is_crawler_url:                                   #该URL已经爬过了
                                        has_more = 0
                                        continue
                                    res = requests.get(url=url,headers=header,proxies=proxies,timeout=timeout)
                                    time.sleep(random.uniform(0.5, 1))
                                    count += 1

                                    item = {'city': city, 'type': ty, 'dist': dist}
                                    total = 0
                                    data = {}
                                    try:
                                        data = res.json()['data']['list']
                                        total = res.json()['data']['total']
                                        totals += len(data)
                                        house_counts += len(data)
                                        print('data: %s, total: %s' %(len(data),total))
                                        if self._parse_record(data, item, is_inserted_data, headers=header, proxies=proxies,timeout=timeout):        #写入数据库
                                            store_url = ('url',store_url)
                                            self.db.insert_one(store_url, table_name=table_url)

                                    except Exception as e:
                                        logger.error("%s in %s" %(e,url))
                                        print("proxy:%s headers:%s error:%s in %s" %(proxies, header,e,url))
                                        time.sleep(random.uniform(10,20))

                                    idx += 1
                                    if totals == total or len(data) == 0:         #爬取到一个区休息
                                        logger.info('成功爬取{}市{}-{}的{}的数据！'.format(city, dist, bc_name, ty))
                                        print('成功爬取{}市{}-{}的{}的数据！'.format(city, dist, bc_name, ty))
                                        time.sleep(random.uniform(1, 1.5))
                                        totals = 0
                                        has_more = 0

                                except Exception as e:
                                    logger.error(e)
                                    return -1
                                    # print('链接访问不成功，正在重试！')

    def _parse_record(self, data, item, is_inserted_data, headers, proxies,timeout):
        """
        解析函数，用于解析爬回来的response的json数据
        :param data: 一个包含房源数据的列表
        :param item: 传递字典
        :param is_inserted_data: 一个集合，存放者已经在数据库中的数据
        :param headers:请求头
        :param proxies:代理IP
        :param timeout: requests.get(timeout)
        :return: 全部成功返回1，有失败的返回0
        """
        result = 1
        if len(data) > 0:
            count = 0
            for rec in data:
                # print(rec)
                item['m_url'] = rec.get('m_url')
                if item['m_url'] in is_inserted_data:
                    continue
                item['bedroom_num'] = rec.get('frame_bedroom_num')
                item['hall_num'] = rec.get('frame_hall_num')
                item['bathroom_num'] = rec.get('layout')[-2]
                item['rent_area'] = rec.get('rent_area')
                item['house_title'] = rec.get('house_title')
                item['resblock_name'] = rec.get('resblock_name')
                item['bizcircle_name'] = rec.get('bizcircle_name')
                item['layout'] = rec.get('layout')
                item['rent_price_listing'] = rec.get('rent_price_listing')
                item['house_tag'] = self._parse_house_tags(rec.get('house_tags'))
                item['frame_orientation'] = rec.get('frame_orientation')
                item['rent_price_unit'] = rec.get('rent_price_unit')

                if count >= 50:          #每次爬取50条数据随机跳转到其他页面，并休眠一段时间
                    proxies = self.get_random_proxy(proxypool_url)  # 代理IP
                    header = self.get_headers(headers=headers, agent_list=user_agent_list)
                    index = random.choice(range(0, 20))
                    cy = random.choice(cities)
                    url = self.get_url(index, cy)
                    requests.get(url, headers=header, proxies=proxies, timeout=timeout)
                    time.sleep(random.uniform(0.1, 0.15))
                    count = 0


                try:
                    res2 = requests.get(item['m_url'],headers=headers,proxies=proxies, timeout=timeout)
                    count += 1
                    pa_lon = r"longitude: '(.*)',"
                    pa_lat = r"latitude: '(.*)'"
                    pa_distance = r"<span class=\"fr\">(\d*)米</span>"
                    item['longitude'] = re.findall(pa_lon, res2.text)[0]
                    item['latitude'] = re.findall(pa_lat, res2.text)[0]
                    distance = re.findall(pa_distance, res2.text)
                    if len(distance) > 0:
                        item['distance'] = distance[0]
                    else:
                        item['distance'] = None
                except:
                    item['longitude'] = None
                    item['latitude'] = None
                    item['distance'] = None

                # self.db['zufang'].update_one({'m_url': item['m_url']}, {'$set': item}, upsert=True)
                if not self.db.insert_data(data=item):
                    result = 0
        return result



    @staticmethod
    def _parse_house_tags(house_tag):
        """
        处理house_tags字段，相当于数据清洗
        :param house_tag: house_tags字段的数据
        :return: 处理后的house_tags
        """
        if len(house_tag) > 0:
            st = ''
            for tag in house_tag:
                st += tag.get('name') + ' '
            return st.strip()

    @staticmethod
    def _write_bc(bc_list):
        """
        把爬取的商圈写入txt，为了整个爬取过程更加可控
        :param bc_list: 商圈list
        :return: None
        """
        with open('./data/crawler/bc_list.txt', 'w') as f:
            for bc in bc_list:
                f.write(bc+'\n')

    @staticmethod
    def _read_bc():
        """
        读入商圈
        :return: None
        """
        with open('./data/crawler/bc_list.txt', 'r') as f:
            return [bc.strip() for bc in f.readlines()]


if __name__ == '__main__':
    rent = Rent(db)
    try:
        logger.info("*******开始爬取*******")
        rent.get_data()
        is_crawler_counts = db.get_counts()
        msg_text = "运行结束, 已经爬取到%d条" % (is_crawler_counts)
        msg_subject = 'house_data_crawler'
        mail(msg_text=msg_text, msg_subject=msg_subject)
    except Exception as e:
        logger.error(e)
        exit(-1)
