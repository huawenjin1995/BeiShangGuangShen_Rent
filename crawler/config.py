#coding: utf-8

rent_type = {'整租': 200600000001, '合租': 200600000002}

city_info = {'北京': [110000, 'bj', {'东城': 'dongcheng', '西城': 'xicheng', '朝阳': 'chaoyang', '海淀': 'haidian',
                                   '丰台': 'fengtai', '石景山': 'shijingshan', '通州': 'tongzhou', '昌平': 'changping',
                                   '大兴': 'daxing', '亦庄开发区': 'yizhuangkaifaqu', '顺义': 'shunyi', '房山': 'fangshan',
                                   '门头沟': 'mentougou', '平谷': 'pinggu', '怀柔': 'huairou', '密云': 'miyun',
                                   '延庆': 'yanqing'}],
             '上海': [310000, 'sh', {'静安': 'jingan', '徐汇': 'xuhui', '黄浦': 'huangpu', '长宁': 'changning',
                                   '普陀': 'putuo', '浦东': 'pudong', '宝山': 'baoshan', '闸北': 'zhabei',
                                   '虹口': 'hongkou','杨浦': 'yangpu', '闵行': 'minhang', '金山': 'jinshan',
                                   '嘉定': 'jiading','崇明': 'chongming', '奉贤': 'fengxian', '松江': 'songjiang',
                                   '青浦': 'qingpu'}],
             '广州': [440100, 'gz', {'天河': 'tianhe', '越秀': 'yuexiu', '荔湾': 'liwan', '海珠': 'haizhu', '番禺': 'panyu',
                                   '白云': 'baiyun', '黄埔': 'huangpu', '从化': 'conghua', '增城': 'zengcheng',
                                   '花都': 'huadu', '南沙': 'nansha'}],
             '深圳': [440300, 'sz', {'罗湖区': 'luohuqu', '福田区': 'futianqu', '南山区': 'nanshanqu',
                                   '盐田区': 'yantianqu', '宝安区': 'baoanqu', '龙岗区': 'longgangqu',
                                   '龙华区': 'longhuaqu', '光明区': 'guangmingqu', '坪山区': 'pingshanqu',
                                   '大鹏新区': 'dapengxinqu'}]}


#城市列表
cities = ['bj', 'sh', 'nj', 'wh', 'cd', 'xa','hf','sz', 'gz']

#***请求的headers
headers = {
# 'Accept':'*/*',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
# 'Cache-Control':'no-cache',
'Connection':'close',
# 'Host':'s1.ljcdn.com',
# 'Origin':'https://m.ke.com',
# 'Pragma':'no-cache',
'Referer':'https://m.lianjia.com',
# 'Sec-Fetch-Dest':'script',
# 'Sec-Fetch-Mode':'cors',
# 'Sec-Fetch-Site':'cross-site',
}

#user_agent 集合
user_agent_list = [
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
 # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
 'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
 # 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
 # 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
 # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
 # 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
 # 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
 # Opera
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Opera/8.0 (Windows NT 5.1; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
# Firefox
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
"Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
# Safari
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
# chrome
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
# 360
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
# 淘宝浏览器
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
# 猎豹浏览器
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
# "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
# QQ浏览器
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
# sogou浏览器
# "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
# maxthon浏览器
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36"

]


#***连接Mysql数据库参数***
host = 'localhost'                  # 数据库地址
port = 3306                         # 端口
username = 'root'                   # 用户名
password = '******'             # 密码
charset = 'utf8mb4'
database = 'BSGS_Rent'              # 数据库名
table_name = 'zufang'
table_url = 'zufang_url'
#********************************

#***添加邮件服务器的信息***
MAIL_SERVER = 'smtp.qq.com'         # 邮箱服务器
MAIL_PORT = 25                      # 服务器端口
MAIL_USE_TLS = 0                    # 电子邮件服务器凭证
MAIL_USERNAME = '1163824714@qq.com' # 发送者邮箱
MAIL_PASSWORD = 'mcoaejbkdxggghef'  # 发送者邮箱登录密码
ADMINS = ['1163824714@qq.com']      # 接受者邮箱列表
#********************************

#***代理池地址****
proxypool_url = 'http://127.0.0.1:5555/random'
#*********************************
