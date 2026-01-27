import pandas as pd
import numpy as np
import os
from pathlib import Path
import time

class RawDataThickness():

    def __init__(self):
        self.filename = None
        self.file = None


    def parse(self,filepath,csvpath):
        self.filepath = filepath
        self.csvpath = csvpath
        files = os.listdir(filepath)
        p = Path(filepath)
        for file_name in p.rglob('*.xlsx'):
            # 使用pd读取excel数据
            print(file_name)
            oridata = pd.read_excel(file_name, sheet_name=0, header=None)
            data = np.array(oridata)
            array_a = list(range(5, 43, 6))
            array_b = list(range(48, 90, 6))
            array_c = array_a + array_b
            index_row = []
            index_col = []
            list_voltage = [[] for i in range(len(array_c))]
            list_capacity = [[] for k in range(len(array_c))]
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if isinstance((data[i][j]), str) == True:
                        if (data[i][j])[-3:] == (str('(1)')):
                            print(data[i][j])
                            print(i, j)
                            index_row.append(i)
                            index_col.append(j)
            current = data[(index_row[1] + 2)][5]
            for i in range(len(index_row)):
                if i in array_c:
                    Nox = array_c.index(i)
                    voltage = np.array(oridata.iloc[(index_row[i] + 2):(index_row[i + 1] - 1), 4])
                    capacity = np.array(oridata.iloc[(index_row[i] + 2):(index_row[i + 1] - 1), 6])
                    voltage2 = list(voltage / 1000)
                    capacity2 = list(capacity / (abs(current) * 1) * 100)  # 看是什么倍率放电，就在此处除以几
                    for x in range(len(voltage2)):
                        list_voltage[len(array_c) - Nox - 1].append(voltage2[x])
                        list_capacity[len(array_c) - Nox - 1].append((capacity2[x]))

            max_len = max((len(l) for l in list_voltage))  # 首先获取list_voltage当中所有元组的长度值，并取最大值
            # 生成一个新矩阵，填充数字0以补齐长度较短的数组，形成一个n阶矩阵
            new_matrix = list(map(lambda l: l + [0] * (max_len - len(l)), list_voltage))
            list_voltage = list(zip(*new_matrix[::-1]))  # 将新矩阵进行转置
            df_voltage = pd.DataFrame(list_voltage)  # 转换为pandas中的dataframe格式，便于后面写入excel
            df_voltage = df_voltage.replace(0, np.nan)  # 将dataframe中的0值转换为Nan值
            max_len1 = max((len(l) for l in list_capacity))  # 首先获取list_capacity当中所有元组的长度值，并取最大值
            # 生成一个新矩阵，填充数字0以补齐长度较短的数组，形成一个n阶矩阵
            new_matrix1 = list(map(lambda l: l + [0] * (max_len1 - len(l)), list_capacity))
            list_capacity = list(zip(*new_matrix1[::-1]))  # 将新矩阵进行转置
            df_capacity = pd.DataFrame(list_capacity)  # 转换为pandas中的dataframe格式，便于后面写入excel
            df_capacity = df_capacity.replace(0, np.nan)  # 将dataframe中的0值转换为Nan值
            df_voltage.to_excel((csvpath + (str(file_name)[-12:-6])+ ('voltage') + ('.xlsx')), sheet_name='Sheet1', index=False)
            df_capacity.to_excel((csvpath + (str(file_name)[-12:-6])+ ('soc') + ('.xlsx')), sheet_name='Sheet1', index=False)



def main():
    start = time.time()

    filepath = "../data/测厚/"
    csvpath = "../processing_data/测厚/"
    X = RawDataThickness()
    X.parse(filepath, csvpath)

    end = time.time()
    runTime = end - start
    print('运行时间：', runTime, 'S')  # 计算运行时间

if __name__ == '__main__':
    main()
