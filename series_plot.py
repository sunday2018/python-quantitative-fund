import  matplotlib.pyplot as plt
import numpy as np
from pandas import Series, DataFrame


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False


s1 = Series(np.random.randn(1000)).cumsum()
s2 = Series(np.random.randn(1000)).cumsum()
print(s1, '\n')
print(s2, '\n')

s1.plot(kind='line', grid=True, label='s1', title='this is series', style='--')
s2.plot(label='s2')
plt.legend()
plt.show()