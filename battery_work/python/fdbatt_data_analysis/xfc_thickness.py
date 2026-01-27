import pandas as pd
import numpy as np
import time
import cal_deriv
import datetime
# from datetime import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
'''打开选择文件夹对话框'''
root = tk.Tk()
root.withdraw()
# Folderpath = filedialog.askdirectory() # 获得选择好的文件夹
Filepath = filedialog.askopenfilename() # 获得选择好的文件
# 使用pd读取excel数据
data = pd.read_excel('../data/厚度仪data/测厚仪数据230629.xlsx')
data2 =pd.read_excel(Filepath)
file = open("../processing_data/石墨DOE/测厚xfc-soc.csv", "w")
file_yp = open("../processing_data/石墨DOE/测厚xfcthickness_gradient.csv", "w")
file_thickness = open("../processing_data/石墨DOE/测厚xfc-thickness.csv", "w")
a = list(range(7,91,6))
b = list(range(8,90,6))
time00 = (data2.iloc[a,3]).tolist()
timelen =(data2.iloc[b,5]).tolist()
time_onset = []
time_ends = []
print(time00)   # .iloc方法读出来的就是timestamp格式，可以相加减
print(timelen)
for i in range(len(time00)):
    time00[i] = time00[i] + datetime.timedelta(minutes=3)   # 两个仪器的时间是不是永远都是相差4分10秒
    time_end = time00[i] + datetime.timedelta(minutes=1) + datetime.timedelta(minutes=timelen[i])
    time_onset.append(time00[i])
    time_ends.append(time_end)
'''
date_all = np.array(data.iloc[:,1])
time_all = np.array(data.iloc[:,2])
date_time = np.array(data.iloc[:,3])
thickness_7_5 =np.array(data.iloc[:,4])
'''
date_all =(data.iloc[:,1]).tolist()
time_all = (data.iloc[:,2]).tolist()
date_time = (data.iloc[:,3]).tolist()
thickness_7_5 =(data.iloc[:,6]).tolist()
C_rate = [0.33333,0.33333,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6]
all_data = [[] for i in range(3)]
# soc_all_data =[]
# thickness_change_all_data = []
# 找第二次0.3333C充电时的最终充电倍率来归一化
date_lyp_033C = []
for j in range(len(date_time)):
    if date_time[j] >= (time_onset[1]) and \
       date_time[j] <= (time_ends[1] + datetime.timedelta(seconds=10))\
            and (thickness_7_5[j]-thickness_7_5[j+1] < 0
            or  thickness_7_5[j]- thickness_7_5[j - 1] > 0):  # 厚度下降条件可以避免选择厚度开始下降之后的数据
       date_lyp_033C.append(j)
print(date_lyp_033C)
time_lyp_normalize = (date_time[date_lyp_033C[-1]] - date_time[date_lyp_033C[0]]) / np.timedelta64(1, "s")
soc_real_normalize = time_lyp_normalize / 3600 * 0.33333 * 100
print(soc_real_normalize)
# 找到所有倍率的充电倍率曲线
for i in range(len(time_onset)):
    date_index = []
    time_change = []
    thickness_change = []
    soc_real = []
    C = C_rate[i]
    basic_thickess = []
    for j in range(len(date_time)):
        if date_time[j] >= time_onset[i] and \
                date_time[j] <= (time_ends[i] + datetime.timedelta(seconds=10)):
            if (thickness_7_5[j] - thickness_7_5[j + 1] < 0
                     or thickness_7_5[j] - thickness_7_5[j - 1] >0):
                date_index.append(j)
    for k in range(len(date_index)):
        n = date_index[k]
        time_delta = (date_time[n] - date_time[date_index[0]]) / np.timedelta64(1, "s")
        # time_real = (time_delta.astype("timedelta[s]") )* 3600 * 24 / 86400000000000
        time_real = time_delta
        soc_real0 = (time_real / 3600 * C * 100)/soc_real_normalize*100
        change00 = (thickness_7_5[n] - thickness_7_5[date_index[0]]) / (thickness_7_5[date_index[0]] - 30044) * 100
        thickness_change.append(change00)
        thicknessA = thickness_7_5[n]
        basic_thickess.append(thicknessA)
        time_change.append(time_real)
        soc_real.append(soc_real0)
    all_data[0].append(soc_real)
    all_data[1].append(thickness_change)
    all_data[2].append(basic_thickess)
print(all_data[0])
# 首先获取list_b当中所有元组的长度值，并取最大值
max_len = max((len(l) for l in all_data[0]))
# 生成一个新矩阵，填充数字0以补齐长度较短的数组，形成一个n阶矩阵
new_matrix = list(map(lambda l:l + [0]*(max_len - len(l)),all_data[0]))
# 将新矩阵进行转置
list_c = list(zip(*new_matrix[::-1]))
# 将list_c当中元素写入txt文件，其中数值不等于0的直接写入，数值等于0的以nan填充（画图的时候origin不会将nan当数值处理）
for i in range(len(list_c)):
    for j in range(14):
        if (list_c[i][14- j - 1] != 0):
           file.write(str(list_c[i][ 14- j - 1]) + '   ')
        if (list_c[i][14 - j - 1] == 0):
           file.write('nan      ')
    file.write('\n')  # 换行
file.close()
# 将厚度变化率写入txt
max_len_yp = max((len(l) for l in all_data[1]))
new_matrix_yp = list(map(lambda l:l + [0]*(max_len_yp - len(l)),all_data[1]))
list_yp = list(zip(*new_matrix_yp[::-1]))
for i in range(len(list_yp)):
    for j in range(14):
        if (list_yp[i][14- j - 1] != 0):
           file_yp.write(str(list_yp[i][ 14- j - 1]) + '   ')
        if (list_yp[i][14- j - 1] == 0):
            file_yp.write('nan      ')
    file_yp.write('\n')  # 换行
file_yp.close()
# 将厚度写入txt
max_len_yp1 = max((len(l) for l in all_data[2]))
new_matrix_yp1 = list(map(lambda l:l + [0]*(max_len_yp1 - len(l)),all_data[2]))
list_yp1 = list(zip(*new_matrix_yp1[::-1]))
for i in range(len(list_yp1)):
    for j in range(14):
        if (list_yp1[i][14- j - 1] != 0):
           file_thickness.write(str(list_yp1[i][ 14- j - 1]) + ',')
        if (list_yp1[i][14- j - 1] == 0):
            file_thickness.write('nan      ')
    file_thickness.write('\n')  # 换行
file_thickness.close()
# 开始画图
fig, ax = plt.subplots(dpi=600)
fig.subplots_adjust(right=0.75)
# ax.plot(all_data[0][0], all_data[1][0], label='0.3333C')
ax.plot(all_data[0][1], all_data[1][1], label='0.3333C')
ax.plot(all_data[0][2], all_data[1][2], label='0.5C')
ax.plot(all_data[0][3], all_data[1][3], label='1C')
ax.plot(all_data[0][4], all_data[1][4], label='1.5C')
ax.plot(all_data[0][5], all_data[1][5], label='2C')
ax.plot(all_data[0][6], all_data[1][6], label='2.5C')
ax.plot(all_data[0][7], all_data[1][7], label='3C')
ax.plot(all_data[0][8], all_data[1][8], label='3.5C')
ax.plot(all_data[0][9], all_data[1][9], label='4C')
ax.plot(all_data[0][10], all_data[1][10], label='4.5C')
ax.plot(all_data[0][11], all_data[1][11], label='5C')
ax.plot(all_data[0][12], all_data[1][12], label='5.5C')
ax.plot(all_data[0][13], all_data[1][13], label='6C')
# ax.plot(all_data[0][14], all_data[1][14], label='6.5C')
ax.set_xlabel("SOC/%")
ax.set_ylabel("Thickness_change/%")
ax.set_xlim(0, 100)
ax.set_ylim(-0.1, 2.0)
ax.legend(loc='upper left',fontsize =8)
plt.savefig('../figure/石墨DOE/xfc_ex.tiff',bbox_inches ='tight')
plt.show()






