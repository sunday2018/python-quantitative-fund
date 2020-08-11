import  matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False


year = [2009,2010,2011,2012,2013]
x = [13,32,54,22,41]
y = [2.1,4.3,5.2,1.5,3.8]

plt.plot(year,x, '.-', label='第一季度')
plt.plot(year, y, '.-', label='第二季度')
# plt.plot(year,y,'ok')
# plt.xlim(2009, 2018)
# plt.ylim(0,50)
plt.title('show')
plt.xlabel('num')
plt.ylabel('age')
plt.legend()
plt.show()