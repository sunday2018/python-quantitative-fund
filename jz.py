# 导入需要的模块
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


# 处理乱码
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False




def get_html(code, start_date, end_date, page=1, per=20):
	url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&page={1}&sdate={2}&edate={3}&per={4}'.format(
		code, page, start_date, end_date, per)
	res = requests.get(url)
	html = res.text
	return html


def get_fund(code, start_date, end_date, page=1, per=20):
	# 获取html
	html = get_html(code, start_date, end_date, page, per)
	soup = BeautifulSoup(html, 'html.parser')
	# 获取总页数
	pattern = re.compile('pages:(.*),')
	result = re.search(pattern, html).group(1)
	total_page = int(result)
	# 获取表头信息
	heads = []
	for head in soup.findAll("th"):
		heads.append(head.contents[0])



	# 数据存取列表
	records = []
	# 获取每一页的数据
	current_page = 1
	while current_page <= total_page:
		html = get_html(code, start_date, end_date, current_page, per)
		soup = BeautifulSoup(html, 'html.parser')
		# 获取数据
		for row in soup.findAll("tbody")[0].findAll("tr"):
			row_recodes = []
			for record in row.findAll('td'):
				val = record.contents
				# 处理空值
				if val == []:
					row_recodes.append(np.nan)
				else:
					row_recodes.append(val[0])
			# 记录数据
			records.append(row_recodes)
		# 下一页
		current_page = current_page + 1


	# 将数据转换为Dataframe对象
	np_records = np.array(records)
	fund_df = pd.DataFrame()
	for col, col_name in enumerate(heads):
		fund_df[col_name] = np_records[:, col]


	# 按日期排序
	fund_df['净值日期'] = pd.to_datetime(fund_df['净值日期'], format='%Y/%m/%d')
	fund_df = fund_df.sort_values(by='净值日期', axis=0, ascending=True).reset_index(drop=True)
	fund_df = fund_df.set_index('净值日期')


	# 数据类型处理
	fund_df['单位净值'] = fund_df['单位净值'].astype(float)
	fund_df['累计净值'] = fund_df['累计净值'].astype(float)
	fund_df['日增长率'] = fund_df['日增长率'].str.strip('%').astype(float)
	return fund_df


if __name__ == '__main__':
	fund_df = get_fund('159905', start_date='2020-02-01', end_date='2020-06-30')
	print(fund_df)
	fig, axes = plt.subplots(nrows=2, ncols=1)
	fund_df[['单位净值', '累计净值']].plot(ax=axes[0])
	fund_df['日增长率'].plot(ax=axes[1])
	plt.show()
