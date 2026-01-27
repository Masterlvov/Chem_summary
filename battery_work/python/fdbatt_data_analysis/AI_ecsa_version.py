import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import glob
from scipy.optimize import leastsq
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 常量定义
ELECTRODE_AREA = 46.6  # 电极面积 (cm²)
CURRENT_CONVERSION_FACTOR = 100  # 电流转换系数

class ECSAAnalyzer:
    """ECSA数据分析器，用于计算双电层电容(CdI)"""
    
    def __init__(self, data_dir, output_dir):
        """
        初始化ECSA分析器
        
        参数:
            data_dir: 原始数据文件目录
            output_dir: 结果输出目录
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)  # 确保输出目录存在
        
    @staticmethod
    def linear_func(params, x):
        """线性函数 y = k*x + b"""
        k, b = params
        return k * x + b
    
    @staticmethod
    def error_func(params, x, y):
        """误差函数，用于最小二乘法拟合"""
        return ECSAAnalyzer.linear_func(params, x) - y
    
    def find_zero_crossing(self, voltage_data, current_data):
        """
        寻找电压过零点及对应的电流值
        
        返回:
            zero_voltage: 过零点电压
            zero_current: 过零点电流
        """
        zero_voltage = []
        zero_current = []
        
        for i in range(1, len(voltage_data)):
            # 检查电压是否跨过零点
            if voltage_data[i] * voltage_data[i-1] <= 0:
                # 线性插值估算精确的零点
                x1, x2 = voltage_data[i-1], voltage_data[i]
                y1, y2 = current_data[i-1], current_data[i]
                
                if x2 != x1:  # 避免除以零
                    t = -x1 / (x2 - x1)
                    zero_v = 0
                    zero_c = y1 + t * (y2 - y1)
                    
                    zero_voltage.append(zero_v)
                    zero_current.append(zero_c)
        
        return zero_voltage, zero_current
    
    def process_scan_data(self, file_paths, scan_rates, sample_label):
        """
        处理一组扫描速率的数据
        
        参数:
            file_paths: 数据文件路径列表
            scan_rates: 扫描速率数组
            sample_label: 样品标签
            
        返回:
            cdI_value: 计算得到的CdI值
            fig_data: 绘图数据 (scan_rates, current_differences)
        """
        if len(file_paths) != len(scan_rates):
            logger.error(f"文件数量({len(file_paths)})与扫描速率数量({len(scan_rates)})不匹配")
            return None, None
        
        current_differences = []
        
        for i, file_path in enumerate(file_paths):
            try:
                # 读取数据文件
                df = pd.read_csv(file_path, sep='\t')
                voltage_data = df.iloc[1:, 0].astype(float).values
                current_data = df.iloc[1:, 1].astype(float).values
                cycle_data = df.iloc[1:, 2].astype(float).values
                
                # 提取特定循环的数据 (cycle = 2)
                cycle_mask = (cycle_data == 2)
                cycle_voltage = voltage_data[cycle_mask]
                cycle_current = current_data[cycle_mask]
                
                # 寻找过零点
                _, zero_currents = self.find_zero_crossing(cycle_voltage, cycle_current)
                
                if len(zero_currents) >= 2:
                    # 计算电流差值 (取前两个过零点)
                    current_diff = abs(zero_currents[1] - zero_currents[0]) / (2 * ELECTRODE_AREA * CURRENT_CONVERSION_FACTOR)
                    current_differences.append(current_diff)
                else:
                    logger.warning(f"文件 {file_path} 中未找到足够的过零点")
                    current_differences.append(np.nan)
                    
            except Exception as e:
                logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
                current_differences.append(np.nan)
        
        # 移除NaN值并对应调整scan_rates
        valid_indices = ~np.isnan(current_differences)
        valid_scan_rates = scan_rates[valid_indices]
        valid_current_diffs = np.array(current_differences)[valid_indices]
        
        if len(valid_scan_rates) < 2:
            logger.error(f"样品 {sample_label} 有效数据点不足，无法进行拟合")
            return None, None
        
        # 使用最小二乘法拟合直线
        initial_params = [0.0006, 0.0005]  # 初始参数猜测 [k, b]
        try:
            fitted_params, _ = leastsq(self.error_func, initial_params, args=(valid_scan_rates, valid_current_diffs))
            cdI_value = fitted_params[0]  # 斜率为CdI值
        except Exception as e:
            logger.error(f"拟合过程出错: {str(e)}")
            return None, None
        
        # 准备绘图数据
        fig_data = (valid_scan_rates, valid_current_diffs, cdI_value)
        
        return cdI_value, fig_data
    
    def analyze_samples(self, file_pattern, scan_rates, sample_labels, files_per_sample=12):
        """
        分析所有样品
        
        参数:
            file_pattern: 文件匹配模式
            scan_rates: 扫描速率数组
            sample_labels: 样品标签列表
            files_per_sample: 每个样品对应的文件数量
        """
        # 获取所有数据文件
        try:
            all_files = sorted(glob.glob(str(self.data_dir / file_pattern)))
        except Exception as e:
            logger.error(f"无法读取数据文件: {str(e)}")
            return
        
        n_samples = len(sample_labels)
        expected_files = n_samples * files_per_sample
        
        if len(all_files) < expected_files:
            logger.warning(f"找到 {len(all_files)} 个文件，但预期 {expected_files} 个文件")
        
        results = {}
        
        for i, label in enumerate(sample_labels):
            start_idx = i * files_per_sample
            end_idx = start_idx + files_per_sample
            
            if end_idx > len(all_files):
                logger.error(f"样品 {label} 文件不足")
                continue
            
            sample_files = all_files[start_idx:end_idx]
            logger.info(f"处理样品 {label}: {len(sample_files)} 个文件")
            
            cdI_value, fig_data = self.process_scan_data(sample_files, scan_rates, label)
            
            if cdI_value is not None:
                results[label] = cdI_value
                
                # 保存结果到Excel
                self.save_results(label, fig_data)
                
                # 绘制图表
                self.plot_results(label, fig_data)
        
        # 打印所有结果
        logger.info("分析完成，结果如下:")
        for label, value in results.items():
            logger.info(f"{label}: CdI = {value:.6e}")
        
        return results
    
    def save_results(self, sample_label, fig_data):
        """保存结果到Excel文件"""
        scan_rates, current_diffs, cdI_value = fig_data
        
        output_data = {
            'Scan_Rate': scan_rates,
            'Current_Difference': current_diffs,
            'CdI': [cdI_value] * len(scan_rates)
        }
        
        df = pd.DataFrame(output_data)
        output_path = self.output_dir / f"{sample_label}_results.xlsx"
        
        try:
            df.to_excel(output_path, index=False)
            logger.info(f"结果已保存到 {output_path}")
        except Exception as e:
            logger.error(f"保存结果到Excel时出错: {str(e)}")
    
    def plot_results(self, sample_label, fig_data):
        """绘制结果图表"""
        scan_rates, current_diffs, cdI_value = fig_data
        
        plt.figure(figsize=(10, 6))
        plt.plot(scan_rates, current_diffs, 'bo', label='实验数据')
        
        # 绘制拟合直线
        x_fit = np.linspace(min(scan_rates), max(scan_rates), 100)
        y_fit = self.linear_func([cdI_value, 0], x_fit)  # 假设截距为0
        
        plt.plot(x_fit, y_fit, 'r-', label=f'拟合直线 (CdI = {cdI_value:.4e})')
        
        plt.xlabel('扫描速率 (mV/s)')
        plt.ylabel('电流差值 (A/cm²)')
        plt.title(f'{sample_label} - 双电层电容分析')
        plt.legend()
        plt.grid(True)
        
        # 保存图表
        plot_path = self.output_dir / f"{sample_label}_plot.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"图表已保存到 {plot_path}")


def main():
    """主函数"""
    # 配置参数
    DATA_DIR = r"E:\data_analysis\python\电极结构data\ECSA\data\zzz"
    OUTPUT_DIR = r"E:\data_analysis\python\电极结构data\ECSA\processing_data\zzz"
    
    # 扫描速率 (mV/s)
    SCAN_RATES = np.array([5, 10, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200])
    
    # 样品标签
    SAMPLE_LABELS = [
        'R1-10', 'R1-1', 'R1-2', 'R1-3', 'R1-4', 'R1-5', 'R1-6', 'R1-7', 'R1-8', 'R1-9',
        'R2-10', 'R2-1', 'R2-2', 'R2-3', 'R2-4', 'R2-5', 'R2-6', 'R2-7', 'R2-8', 'R2-9',
        'R3-10', 'R3-1', 'R3-3', 'R3-4', 'R3-5', 'R3-6', 'R3-7', 'R3-8', 'R3-9'
    ]
    
    # 创建分析器并运行分析
    analyzer = ECSAAnalyzer(DATA_DIR, OUTPUT_DIR)
    results = analyzer.analyze_samples("*.txt", SCAN_RATES, SAMPLE_LABELS)
    
    return results


if __name__ == '__main__':
    main()
