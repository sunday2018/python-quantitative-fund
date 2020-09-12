'''
格式化脚本
1. 按日期正序排列，去掉无用信息
2. 文件名形如：510880_lsjz_sort.csv
'''


import csv
import sys
from operator import itemgetter


code = '510900'
csv_file = './data/%s_lsjz.csv' % code
sort_csv_file = './data/%s_lsjz_sort.csv' % code
print(csv_file)
print(sort_csv_file)

csv_file_handle = open(csv_file,'r',encoding='utf-8')
sort_csv_file_handle = open(sort_csv_file, 'w',encoding='utf-8', newline='')

table = []
header = csv_file_handle.readline()
for line in csv_file_handle:
	tmp_col = []
	col = line.split(',')
	tmp_col = [col[0].strip(), float(col[1]), float(col[2]), col[3]+'%', col[4], col[5]]
	table.append(tmp_col)

table_sorted = sorted(table, key=itemgetter(0), reverse=False)

header='日期,单位净值,历史净值,日增长率,申购状态,赎回状态\n'
sort_csv_file_handle.write(header)
for row in table_sorted:
	row = [str(x) for x in row]
	new_row = ','.join(row)
	print(new_row)
	sort_csv_file_handle.write(new_row+'\n')

csv_file_handle.close()
sort_csv_file_handle.close()
print('ok')
