import matplotlib.pyplot as plt
# import matplotlib
# import pdb


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 纵坐标与横坐标数据
gdp_rate = [9.4,10.6,9.6,7.9,7.8,7.3,6.9,6.7,6.8,6.6]
first_industry_rate = [4.0,4.3,4.2,4.5,3.8,4.1,3.9,3.3,4.0,3.5]
second_industry_rate = [10.3,12.7,10.7,8.4,8.0,7.4,6.2,6.3,5.9,5.8]
third_industry_rate = [9.6,9.7,9.5,8.0,8.3,7.8,8.2,7.7,7.9,7.6]
years = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
# print(gdp_rate)
# pdb.set_trace()


# 4个plot函数画出4条线，线形为折线，每条线对应的表现label
plt.plot(years, gdp_rate, '.-', label='GDP增长率')
plt.plot(years, first_industry_rate, '.-', label='第一产业增长率')
plt.plot(years, second_industry_rate, '-', label='第二产业增长率')
plt.plot(years, third_industry_rate, '-', label='第三产业增长率')

plt.title('混合折线图示例')
plt.xticks(years) # 横坐标刻度 yticks 纵坐标刻度
plt.xlabel('年份') # 横坐标标题
plt.ylabel('数据')
plt.legend() # 显示图例，即每条线对应label内容
plt.show() # 显示图形
