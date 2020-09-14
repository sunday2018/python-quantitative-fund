# /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import re
import pandas as pd
import math
import time
import random
import csv


'''
 全量抓取

 1. 全量抓取基金净值
 2. 文件名形如：510880_lsjz.csv
'''


def get_one_page(fundcode, pageIndex=1):
    '''
    获取基金净值某一页的html
    :param fundcode: str格式，基金代码
    :param pageIndex: int格式，页码数
    :return: str格式，获取网页内容
    '''
    url = 'http://api.fund.eastmoney.com/f10/lsjz'
    cookie = 'EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=01-24 17:11:50@#$%u957F%u4FE1%u5229%u5E7F%u6DF7%u5408A@%23%24519961; st_pvi=27838598767214; st_si=11887649835514'
    headers = {
        'Cookie': cookie,
        'Host': 'api.fund.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Referer': 'http://fundf10.eastmoney.com/jjjz_%s.html' % fundcode,
    }
    params = {
        'callback': 'jQuery18307633215694564663_1548321266367',
        'fundCode': fundcode,
        'pageIndex': pageIndex,
        'pageSize': 20,
    }
    try:
        r = requests.get(url=url, headers=headers, params=params)
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    '''
    解析网页内容
    :param html: str格式，html内容
    :return: dict格式，获取历史净值和访问页数
    '''
    if html is not None:  # 判断内容是否为None
        content = re.findall('\((.*?)\)', html)[0]  # 提取网页文本内容中的数据部分
        lsjz_list = json.loads(content)['Data']['LSJZList']  # 获取历史净值列表
        total_count = json.loads(content)['TotalCount']  # 获取数据量
        total_page = math.ceil(total_count / 20)  #
        lsjz = pd.DataFrame(lsjz_list)
        info = {'lsjz': lsjz,
                'total_page': total_page}
        # Logger('log/all.log',level='debug').logger.info(info)
        # Logger('log/error.log', level='error').logger.error('error')
        return info
    return None


def main(fundcode):
    '''
    将爬取的基金净值数据储存至本地csv文件
    '''
    html = get_one_page(fundcode)
    info = parse_one_page(html)
    total_page = info['total_page']
    lsjz = info['lsjz']
    new_lsjz = pd.DataFrame(lsjz, columns=['FSRQ', 'DWJZ', 'LJJZ', 'JZZZL', 'SGZT', 'SHZT', 'FHSP'])
    # print(new_lsjz)
    new_lsjz.to_csv('./data/%s_lsjz.csv' % fundcode, index=False, encoding='utf-8')  # 将基金历史净值以csv格式储存
    page = 1
    while page < total_page:
        page += 1
        print(new_lsjz)
        html = get_one_page(fundcode, pageIndex=page)
        info = parse_one_page(html)
        if info is None:
            break
        lsjz = info['lsjz']
        new_lsjz = pd.DataFrame(lsjz, columns=['FSRQ', 'DWJZ', 'LJJZ', 'JZZZL', 'SGZT', 'SHZT', 'FHSP'])
        new_lsjz.to_csv('./data/%s_lsjz.csv' % fundcode, mode='a', index=False, header=False, encoding='utf-8')  # 追加存储
        time.sleep(random.randint(5, 10))



if __name__=='__main__':
    
    fundcode = '510050'
    main(fundcode)