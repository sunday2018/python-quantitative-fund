#  净值增量追加
'''
增量追加脚本：
1. 获取指定时间段内的净值信息，追加到csv文件内
2. 文件名形如：510880_lsjz_sort.cvs
'''

import requests
import re
import numpy as np
from bs4 import BeautifulSoup
import time
from operator import itemgetter
import csv
import time

'''
code = '510300'
url = 'http://fundgz.1234567.com.cn/js/%s.js' % code
result = requests.get(url)
data = json.loads(re.match(".*?({.*}).*", result.text, re.S).group(1))
print('基金名称: %s' % data['name'])
print('净值日期: %s' % data['jzrq'])
print('单位净值: %s' % data['dwjz'])

# 输出结果如下：
# 基金名称: 华泰柏瑞沪深300ETF
# 净值日期: 2020-08-31
# 单位净值: 4.8822
'''

def get_url(url, params=None, proxies=None):
	rsp= requests.get(url, params=params, proxies=proxies)
	rsp.raise_for_status()
	return rsp.text


def get_fund_data(code, start='', end=''):
	# record = {'Code': code}
	url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
	params = {'type':'lsjz', 'code':code, 'page': 1, 'per':65535, 'sdate':start, 'edate':end}
	# url = '?type=lsjz&code=510880&page=1&sdate=2020-08-14&edate=2020-09-10&per=20'
	html = get_url(url, params)
	soup = BeautifulSoup(html, 'html.parser')

	# 获取总页数
	pattern = re.compile(r'pages:(.*),')
	result = re.search(pattern, html).group(1)
	pages = int(result)

	#获取表头
	heads = []
	for head in soup.findAll('th'):
		heads.append(head.contents[0])

	# 获取净值列表
	records = []
	page = 1
	while page <= pages:
		params = {'type':'lsjz', 'code':code, 'page':page, 'per':65535, 'sdate':start, 'edate':end}
		html = get_url(url, params)
		soup = BeautifulSoup(html, 'html.parser')

		for row in soup.findAll('tbody')[0].findAll('tr'):
			row_recodes = []
			for record in row.findAll('td'):
				val = record.contents

				if val == []:
					row_recodes.append('')
				else:
					row_recodes.append(val[0])

			records.append(row_recodes)
		page = page+1

	return records
	


def demo(code, start, end):
	records = get_fund_data(code, start, end)
	records_sorted = sorted(records, key=itemgetter(0), reverse=False)
	return records_sorted


if __name__ == "__main__":

	code = 510900
	sdate = '2020-08-14'
	edate = '2020-09-10'

	# 定义新文件名称
	today = time.strftime('%Y-%m-%d', time.localtime())
	new_csv_file = '%s_lsjz_%s.csv' % (code , today)
	# print(new_csv_file)

	# 获取上次保存的最后一条记录日期
	last_write_date = ''
	csv_file = '%s_lsjz_sort.csv' % code
	with open(csv_file, 'r', encoding='utf-8') as fp:
		lines = fp.readlines()
		last_line = lines[-1]
		last_line_arr =last_line.split(',')
		last_write_date = last_line_arr[0]

	print(last_write_date)
	
	print( 'ok')