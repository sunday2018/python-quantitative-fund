# coding=utf8
import csv

f = csv.reader(open('test.csv', 'r'))
for i in f:
	print(i)
