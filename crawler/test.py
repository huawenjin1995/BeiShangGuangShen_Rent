#coding: utf-8
import requests, random, re
from crawler.house_data_crawler import Rent
from crawler.config import proxypool_url, user_agent_list,headers
from crawler.db_handler import db

class Test(Rent):
    def get_request(self):
        count = 0
        for ty, type_code in self.rent_type.items():  # 整租、合租
            for city, info in self.city_info.items():  # 城市、城市各区的信息
                for dist, dist_py in info[2].items():  # 各区及其拼音
                    proxies = self.get_random_proxy(proxypool_url)  # 代理IP
                    if count >= 20:
                        proxies = self.get_random_proxy(proxypool_url)  # 代理IP
                        count = 0
                    # used_prox.append(proxies)
                    header = self.get_headers(headers=headers, agent_list=user_agent_list)
                    timeout = random.choice(range(10, 30))
                    print(info[1], dist_py)
                    res_bc = requests.get('https://bj.lianjia.com/chuzu/{}/zufang/{}/'.format(info[1], dist_py),
                                          headers=header, proxies=proxies, timeout=timeout)
                    count += 1
                    print(res_bc.status_code)
                    pa_bc = r"data-type=\"bizcircle\" data-key=\"(.*)\" class=\"oneline \">"
                    bc_list = re.findall(pa_bc, res_bc.text)
                    return bc_list





if __name__ == '__main__':
    # test = Test(db)
    # print(test.get_request())


    # result = db.insert_one(url, table_name='zufang_url')
    # print(result)

    # result = db.get_column(column='url', table_name='zufang_url')
    # print(len(result))
    # print(len(set(result)))

    # result = db.get_counts(table_name='zufang')
    # print(result)

    with open('./data/crawler/bc_list.txt', 'w') as f:
        f.write('hello' + '\n')

    with open('./data/crawler/bc_list.txt', 'r') as f:
        for line in f:
            print(line)