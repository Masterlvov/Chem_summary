import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import glob
# 最小二乘法拟合曲线
def func(p, x):
    k, b, = p
    return k * x +b

# 定义标准差
def error(p, x, y):
    return func(p, x) - y

# 求石墨负极ECSA面积
def ecsa(filepath,csvpath,labels):
    xx = np.arange(0,360,12) # 多少个文件360改为多少
    for j in range(len(xx)):
        label = labels[j]
        l = 13   #扫速个数+1
        kk = 0
        list_b = [[] for i in range(l * 2)
        Ewe_zero = []
        Ewe_zero_index = []
        ImA = []
        dIma = []
        p0 = [0.00060609, 0.000553]
        scan_voltage = np.array([5,10,20,40,60,80,100,120,,140,160,180,200])
        cdls = []
        for file in filepath[xx[j]:xx[j]+12]:  # 读取前10个文件
            print(file)
            # 读取txt文件，假设文件是制表符（tab）分隔的，如果是其他分隔符，请相应修改
            df = pd.read_table(file, sep='\t')  # header=None
            # print(df)
            # df_filtered = df[df.iloc[:, 6] == '3.000000000000000E+000']
            file = np.array(df.iloc[1:, [0,1,2]])
            for i in range(len(file[:, 2])):
                if (file[:, 2][i] == 2):
                   list_b[2 * kk].append(file[:, 0][i])
                   list_b[2 * kk + 1].append(file[:, 1][i])
            for i in range(len(list_b[2 * kk])):
                if list_b[2 * kk][i] * list_b[2 *  kk][i - 1] <= 0:
                    Ewe_zero.append(list_b[2 * kk][i])
                    Ewe_zero_index.append(i)
                    ImA.append(list_b[2 * kk + 1][i])
             # print(Ewe_zero_index)
             # print(len(Ewe_zero_index))
             # print(len(ImA))
             kk += 1      
         for i in range(len(scan_voltage)):
             deli = abs(ImA[2 * i + 1] - ImA[2 * i]) / 2 / 46.6 / 100
             dIma.append(deli)
         para = leastsq(error, p0, args=(scan_voltage, dIma))
         k = para[0][0]
         cdls.append(k)
         print(cdls)
         figdata = [scan_voltage, dIma, cdls]
         df = pd.DataFrame(figdata)
         df.to_excel((csvpath + (str(label)) + ('.xlsx')), sheet_name='Sheet1', index=False)
         plt.plot(scan_voltage, dIma, 'b-', marker='o')
         # plt.show()


def main ():
    filepath = glob.glob('E:\data_ aalysis\data_analysis\python\电极结构data\ECSA\data\zzz\/*.txt')  # 修改为你的txt文件目录
    csvpath = "E:\data_ analysis\data_analysis\python\电极结构data\ECSA\processing_data\zzz\\"
    labels = ['R1-10','R1-1','R1-2','R1-3','R1-4','R1-5','R1-6','R1-7','R1-8','R1-9',
              'R2-10','R2-1','R2-2','R2-3', 'R2-4','R2-5','R2-6','R2-7','R2-8','R2-9',
              'R3-10','R3-1','R3-3','R3-4','R3-5', 'R3-6','R3-7','R3-8','R3-9']
    ecsa(filepath,csvpath,labels)


if __name__ == '__main__':
    main()
  
  
          
         
           
       
              

           
                  
        
               
    
          
      
      
                  
 
