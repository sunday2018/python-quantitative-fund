# coding:utf-8
import csv
import codecs

data = [
	('测试1','测试工程师'),
	('测试2','测试工程师'),
	('测试3','测试工程师'),
	('测试4','测试工程师'),
	('测试5','测试工程师')
]
f = codecs.open('test.csv', 'w', 'gbk')
writer = csv.writer(f)
for i in data:
	writer.writerow(i)
f.close()


