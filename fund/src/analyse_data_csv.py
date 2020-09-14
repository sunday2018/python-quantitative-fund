# /usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import numpy as np
import statistics


'''
净值分析

参考值：最大值、最小值、平均值、中位数、众数
区间划分：五分位
波动：标准差
'''


if __name__ == '__main__':

	code = '510050'

	csv_file = './data/%s_lsjz_sort.csv' % code
	csv_file_handle = open(csv_file,'r',encoding='utf-8')

	# 组织净值列表
	lsjz_list = []
	header = csv_file_handle.readline()
	for line in csv_file_handle:
		col = line.split(',')
		# tmp_col = [col[0].strip(), float(col[1]), float(col[2]), col[6]+'%', col[7], col[8]]
		lsjz_list.append(float(col[1]))
	lsjz_list.sort() # 升序
	# print(lsjz_list)


	avg = np.mean(lsjz_list) # 平均值
	bzc = np.std(lsjz_list, ddof=1) # 标准差
	median_val = np.median(lsjz_list) # 中位数
	print('平均值:%s' % round(avg,4))
	print('标准差：%s' % round(bzc))
	print('中位数：%s' % median_val)
	print('len:%s' % len(lsjz_list))
	

	print('-----------')
	
	# 去掉重复值并保持排序不变
	new_list = sorted(set(lsjz_list), key=lsjz_list.index)
	v_max = max(new_list)
	v_min = round(min(new_list),4)
	print('v_max:%s' % v_max)
	print('v_min:%s' % v_min)

	# 去掉最大值和最小值
	print('len:%s' % len(new_list))
	new_list.remove(max(new_list))
	new_list.remove(min(new_list))
	
	print('-----------')
	# 划分五等份，计算步长
	buchang = int(round(len(new_list)/5, 0))
	print('buchang:%s' % buchang)

	# 较低
	index_1 = 0
	index_2 = buchang

	# 低
	index_3 = buchang+1
	index_4 = buchang*2

	# 正常
	index_5 = buchang*2 + 1
	index_6 = buchang*3

	# 高
	index_7 = buchang*3 + 1
	index_8 = buchang * 4

	# 较高
	index_9 = buchang*4 + 1
	index_10 = len(new_list) - 1

	print('[%s - %s][%s - %s][%s - %s][%s - %s][%s - %s]' % (index_1, index_2, index_3, index_4, index_5, index_6, index_7, index_8, index_9, index_10))
	print('[%s - %s][%s - %s][%s - %s][%s - %s][%s - %s]' % (new_list[index_1], new_list[index_2], new_list[index_3], new_list[index_4], new_list[index_5], new_list[index_6], new_list[index_7], new_list[index_8], new_list[index_9], new_list[index_10]))



