#coding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sci

from pandas.io.json import json_normalize

plt.style.use('ggplot')
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  #解决seaborn中文字体显示问题
plt.rc('figure', figsize=(10, 10))  #把plt默认的图片size调大一点
plt.rcParams["figure.dpi"] =mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
#问题：
#1.各城市的租房分布怎么样？
#2.城市各区域的房价分布怎么样？
#3.距离地铁口远近有什么关系？
#4.房屋大小对价格的影响如何？
#5.租个人房源好还是公寓好？
#6.精装和简装对房子价格的影响
#7.北方集中供暖对价格的影响
#8.北上广深租房时都看重什么？

def get_house_dist(data, city):
    '''
    获取城市租房分布情况
    :param data: 清洗后的dataframe
    :param city:一个字符串，要分析的城市
    :return:
    '''

    data = data[['city','dist']]        #取两列
    plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=3.0, wspace=1.0,
                        hspace=0.5)  # 设置各subplot间的间隔

    fig = plt.figure(dpi=300)
    counts = data[data['city'] == city]['dist'].count()     #获取该城市所有房源数量
    label_dis1 = data[data['city'] == city]['dist'].value_counts()      #获取每个区的房源数量
    label_dis2 = data[data['city'] == city]['dist'].value_counts().apply(lambda x: x / counts)      #获取每个区的房源占比

    ax1 = fig.add_subplot(2, 1, 1)
    for tick in ax1.get_xticklabels():
        tick.set_rotation(90)  # 将x轴tick旋转90度

    ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)
    for tick in ax2.get_xticklabels():
        tick.set_rotation(90)  # 将x轴tick旋转90度

    ax1.bar(x=label_dis1.index, height=label_dis1, color='blue')
    ax1.set_title('{}市各区房源数量'.format(city))

    ax2.bar(x=label_dis2.index, height=label_dis2)
    ax2.set_title('{}市各区房源比例'.format(city))

    plt.savefig('../data/house_data_analyze/house_dist/{}.pdf'.format(city))


def get_price_dist(data, city):
    '''
    获取城市各区租房价格分布
    :param data: 经过清洗后的dataframe
    :param city: 城市名称
    :return:
    '''
    data = data[['city','dist','aver_price']]       #取三列

    fig = plt.figure(dpi=300)
    city_data = data[data['city'] == city]
    dists = city_data['dist'].unique()     #获取城市所有区
    aver_prices = []
    for dist in dists:                                      #获取每个区的平均租房价格
        s_price = city_data[city_data['dist'] == dist]['aver_price']
        mean = s_price.mean()                                 #平均价格
        std = s_price.std()                                   #标准差
        # print(s_price.describe())
        price = s_price[(s_price <= mean+3*std) & (s_price >= mean-3*std)]   #去掉异常点后的平均价格
        # print(price.describe())
        aver_price = price.mean()                               #去掉异常点后的均值
        # print(dist,aver_price)
        aver_prices.append(aver_price)

    ax = fig.add_subplot(1, 1, 1)
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)  # 将x轴tick旋转90度

    ax.bar(x=dists, height=aver_prices, color='blue')
    ax.set_title('{}市各区平均租金(元/平方米)'.format(city))
    plt.savefig('../data/house_data_analyze/house_aver_price/{}_dist.pdf'.format(city))


def get_top10_bc(data, city):
    '''
    获取城市top10商圈租房价格分布
    :param data: 经过清洗后的dataframe
    :param city: 城市名称
    :return:
    '''
    top10_bc = data[(data['city']==city)&(data['bizcircle_name']!='')].groupby('bizcircle_name')['aver_price'].mean().nlargest(10)


    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)  # 将x轴tick旋转90度

    ax.bar(x=top10_bc.index, height=top10_bc.values, color='blue')
    ax.set_title('{}市top10商圈平均租金(元/平方米)'.format(city))
    plt.savefig('../data/house_data_analyze/house_aver_price/{}_top10_bc.pdf'.format(city))


def distance_price_relation(city, data):
    '''
    获取租金均价与距离地铁口远近的热力图
    :param data: 经过清洗后的dataframe
    :param city: 城市名称
    :return:
    '''
    valid_data = data[(data['city']==city) &
                            (data['aver_price']<=350)].dropna(subset=['distance'])

    fig = plt.figure(dpi=300)
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2,1,2)

    ax1.scatter(x=valid_data['distance'], y=valid_data['aver_price'])
    ax1.set_xlabel('米')
    ax1.set_ylabel('元/平方米')
    ax1.set_title('{}市平均租金与离地铁站距离散点图'.format(city))

    data = valid_data[(valid_data['city'] == city)].groupby('distance')['aver_price'].mean()
    # print(data)
    ax2.plot(data.index, data.values)
    ax2.set_xlabel('米')
    ax2.set_ylabel('元/平方米')
    ax2.set_title('{}市平均租金与离地铁站距离关系'.format(city))
    plt.savefig('../data/house_data_analyze/house_price_with_distance/{}_jointplot.pdf'.format(city))


def area_price_relation(city, data):
    '''
    分析房屋面积与租金的影响
    :param city: 经过清洗后的dataframe
    :param data: 城市名称rent_area_with_price
    :return:
    '''
    fig = plt.figure(dpi=300)
    data = data[(data['city']==city)&(data['rent_area']<150)].groupby('rent_area')['aver_price'].mean()
    # print(data)

    ax = fig.add_subplot(1,1,1)
    ax.plot(data.index,data.values)
    ax.set_xlabel('平方米')
    ax.set_ylabel('元/平方米')
    ax.set_title('{}市房源面积与租金关系'.format(city))
    plt.savefig('../data/house_data_analyze/rent_area_with_price/{}.pdf'.format((city)))


if __name__ == '__main__':
 from house_data_analyse.data_cleaning import get_clean_data

 data = get_clean_data()
 #获取平均价格
 data['aver_price'] = np.round(data['rent_price_listing'] / data['rent_area'], 1)
 cities = ['北京', '上海', '广州', '深圳']
 for city in cities:
     # get_house_dist(data, city)
     # get_price_dist(data, city)
     # get_top10_bc(data,city)
    distance_price_relation(city, data)
    # area_price_relation(city,data)