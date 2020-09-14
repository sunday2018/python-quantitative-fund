# ./usr/bin/env python
# -*- coding: utf-8 - *-

import os
import requests
import re
import csv
import datetime

'''
增量追加

1. 遍历csv文件，文件名形如：510880_lsjz_sort.cvs
2. 计算起始日期和终止日期
3. 获取增量净值数据
4. 追加增量数据到现有文件中

建议：一周操作一次
'''

# 定义日期通用格式
date_format = '%Y-%m-%d'


def get_url(url, params=None, proxies=None):
	rsp= requests.get(url, params=params, proxies=proxies)
	rsp.raise_for_status()
	return rsp.text

# 获取增量净值数据
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
	

# 保存增量净值数据
def saveAppendData(code, start, end, csv_file):
	records = get_fund_data(code, start, end)
	records_sorted = sorted(records, key=itemgetter(0), reverse=False)

	f = open(csv_file,'a',encoding='utf-8',newline='')
	for row in records_sorted:
		row = [str(x) for x in row]
		new_row = ','.join(row)
		# print(new_row)
		f.write(new_row + '\n')
	f.close()

	print('%s - %s' % (sdate, edate))
	print(csv_file)
	print( 'ok')


def getAllCsvFiles():
	rootdir = './data'
	csv_files = []

	flist = os.listdir(rootdir)
	for i in range(0, len(flist)):
		tmp_str = flist[i].split('sort.csv')[0]
		tmp_indx = flist[i].rfind('sort.csv')
		if tmp_indx < 0:
			continue
		csv_files.append(flist[i])

	return csv_files



if __name__ == "__main__":

	# 昨日日期
	edate = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(date_format)

	csv_file_list = getAllCsvFiles()
	for item_file in csv_file_list:
		tmp_list = item_file.split('_')
		code = tmp_list[0]

		# 获取上次保存的最后一条记录日期
		last_write_date = ''
		csv_file = './data/%s' % item_file
		with open(csv_file, 'r', encoding='utf-8') as fp:
			lines = fp.readlines()
			last_line = lines[-1]
			last_line_arr =last_line.split(',')
			last_write_date = last_line_arr[0]

		# 最后一条记录日期加一天，得到起始日期
		d_last_date = datetime.datetime.strptime(last_write_date, date_format)
		sdate = (d_last_date + datetime.timedelta(days=1)).strftime(date_format)

		saveAppendData(code, sdate, edate, csv_file)