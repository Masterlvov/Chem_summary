import pandas as pd
import numpy as np
import time
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

def derivation_data(x, y):
    f = interp1d(x, y, kind='linear')
    x_new = nplinspace(x.min(), x.max(),  int(len(x)))
    y_new = f(x_new)
    window_length = 10
    polyorder = 2
    y_new = savgol_filter(y_new, window_length, polyorder)
    dy_dx = np.gradient(y_new, x_new)
    return x_new, y_new, dy_dx


class thickness():
    def __init__(self):
        self.filename = None
        self.file = None
    def derivation(self,filepath,csvpath):
        self.filepath = filepath
        self.csvpath = csvpath
        p = Path(filepath)
        for file_name in p.rglob('*.xlsx'):
            print(file_name)
            data = pd.read_excel(file_name,sheet_name=0)
            soc_norm = float(data.iloc[-1, 0])
            numbers_der =[[] for i in range(3*19)]
            for i in range(0,55,3):
                print(i)
                soc_normalization = []
                soc_arrays = data.iloc[:, i].to_numpy().squeeze()
                nan_soc = np.isnan(soc_arrays)
                not_nan_indices = ~nan_soc
                soc_arrays = soc_arrays[not_nan_indices]
                for x in range(len(soc_arrays)):
                    xx = soc_arrays[x]/soc_norm*100
                    soc_normalization.append(xx)
                soc_normalization =np.array(soc_normalization)
                thickness_arrays = data.iloc[:, i + 1].to_numpy().squeeze()
                nan_thickness = np.isnan(thickness_arrays)
                not_nan_indices = ~nan_thickness
                thickness_arrays = thickness_arrays[not_nan_indices]
                x_new, y_new, dy_dx = derivation_data(soc_normalization, thickness_arrays)
                a = int(i / 3) 
                numbers_der[3 * (19 - a) - 1] = x_new.tolist()
                numbers_der[3 * (19 - a) - 2] = y_new.tolist()
                numbers_der[3 * (19 - a) - 3] = dy_dx.tolist()
             max_len = max((len(l) for l in numbers_der))
             new_matrix = list(map(lambda l: l + [0] * (max_len - len(l)), numbers_der))
             list_c = list(zip(*new_matrix[::-1]))
             df = pd.DataFrame(list_c)
             df = df.replace(0, np.nan)
             print(df)
             df.to_excel((csvpath + (str(file_name)[-18:-5]) +('.xlsx')), sheet_name='Sheet1', index=False)
def main():
    start = time.time()
    filepath = r"../processing_data/2025/song2/"
    csvpath =  r"../processing_data/2025/derivation/"
    X = thickness()
    X.derivation(filepath, csvpath)
    end = time.time()
    runTime = end - start
    print('运行时间：', runTime, '秒')


if __name__ == '__main__':
    main()



   
 
          
          
    
              
  
  
              
               
              
              
               
              
              
                  
                 
                  

              
       
              
              
          
            
          
          
       
       
      
      
   
  
    
  
