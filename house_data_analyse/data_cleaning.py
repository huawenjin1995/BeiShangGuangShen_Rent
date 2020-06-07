#coding: utf-8
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from house_data_analyse.config import DATABASE_URL,TABLE


def get_data(database_url, table):
    '''
    从数据路中读取数据
    :param database_url:字符串，连接数据库的URL
    :param table: 查询数据的表
    :return: 返回一个dataframe
    '''
    sql = "select * from %s ;" %table
    engine = create_engine(database_url)
    data = pd.read_sql_query(sql, engine)
    return data


def get_aver(data):
    '''
    有些字段填写的是一个范围，取平均值
    :param data:字符串类型,如'23' , '12-35'
    :return: 返回转换后的data
    '''
    if isinstance(data, str) and '-' in data:
        data = data.split('-')
        low, high = data[0], data[1]
        return (int(low) + int(high)) / 2
    if data == None:
        return 0
    else:
        return int(data)


def dw_None_dis(data):
    '''
    有些数据有None,需要进行处理
    :param data: 要处理的data
    :return:
    '''
    if data is None:
        return np.nan
    else:
        return int(data)


def dw_None_latlon(data):
    '''
        有些数据有None,需要进行处理
        :param data: 要处理的data
        :return:
        '''
    if data is None or data == '':
        return np.nan
    else:
        return float(data)


def drop_columns(data, columns):
    '''
    去掉数据中对分析无用的列
    :param data: 要处理的dataframe
    :param columns: 列表，要去掉的列
    :return: 返回去掉指定列的dataframe
    '''
    data = data.drop(columns=columns)
    return data


def get_clean_data(database=DATABASE_URL, table=TABLE):
    '''
    清洗数据
    :param database_url:字符串，连接数据库的URL
    :param table: 查询数据的表
    :return: 返回一个dataframe
    '''
    #获取数据库中的数据
    data = get_data(database_url=database, table=table)

    #去掉一些无用的列
    unuseed_columns = ['id', 'rent_price_unit']
    data = drop_columns(data=data, columns=unuseed_columns)

    # 将租住面积'rent_area'转换为整数,并去掉面积<5 的数据
    data['rent_area'] = data['rent_area'].apply(get_aver)
    data = data.drop(data[data['rent_area'] < 5].index)

    # 价格是有区间的，需要按照处理rent_area一样的方法处理
    data['rent_price_listing'] = data['rent_price_listing'].apply(get_aver)

    # 数据类型转换
    for col in ['bathroom_num', 'bedroom_num', 'hall_num', 'rent_price_listing']:
        data[col] = data[col].astype(int)

    #将'bedroom'转换为int类型，并去掉'bedroom_num' <=0的数据（房间数要>0）
    data = data.drop(data[data['bedroom_num'] <= 0].index)

    # 'distance'(离最近地铁站距离，/米）, 'latitude'（维度）, 'longitude'（经度)因为有None，需另外处理
    data['distance'] = data['distance'].apply(dw_None_dis)
    data['latitude'] = data['latitude'].apply(dw_None_latlon)
    data['longitude'] = data['longitude'].apply(dw_None_latlon)

    return data


if __name__ == '__main__':
    data = get_clean_data()
    print(data.info())