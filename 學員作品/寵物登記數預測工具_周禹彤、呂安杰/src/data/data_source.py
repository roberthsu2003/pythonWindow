import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import threading

@dataclass
class CountyStats:
    """縣市統計資料結構類別"""
    county: str  # 縣市名稱
    years: np.ndarray  # 年份陣列
    registrations: np.ndarray  # 登記數陣列
    deregistrations: np.ndarray  # 註銷數陣列
    neutered: np.ndarray  # 絕育數陣列
    neutering_rates: np.ndarray  # 絕育率陣列
    
    @property
    def records(self) -> List[Tuple]:
        """將資料轉換為記錄格式"""
        return [
            (year, self.county, reg, dereg, neu, rate)
            for year, reg, dereg, neu, rate in zip(
                self.years,
                self.registrations,
                self.deregistrations,
                self.neutered,
                self.neutering_rates
            )
        ]

class PetDataManager:
    """寵物資料管理類別,負責資料的快取與高效能處理"""
    
    def __init__(self, csv_file: str = '2023-2009pet_data.csv'):
        """
        初始化資料管理器
        
        Args:
            csv_file: CSV 資料檔案路徑
        """
        # 定義縣市順序，將全臺加入第一位
        self._county_order = [
            "全臺",  # 加入全臺作為第一個選項
            "基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", 
            "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市",
            "嘉義縣", "臺南市", "高雄市", "屏東縣", "臺東縣", "花蓮縣",
            "宜蘭縣", "澎湖縣", "金門縣", "連江縣"
        ]
        
        # 初始化執行緒相關物件
        self._lock = threading.Lock()  # 執行緒鎖
        self._stats_cache = {}  # 統計資料快取
        self._executor = ThreadPoolExecutor(max_workers=4)  # 執行緒池
        
        # 初始化資料
        self._initialize_data(csv_file)
        
    def _initialize_data(self, csv_file: str):
        """初始化資料,使用並行處理提升效能"""
        # 讀取CSV檔案，並指定資料型別以優化記憶體使用
        self.df = pd.read_csv(
            csv_file,
            dtype={
                'Year': np.int32,
                'Registrations': np.int32,
                'Deregistrations': np.int32,
                'Neutered': np.int32,
                'Neutering Rate': np.float32
            }
        )
        
        # 資料預處理與排序
        self.df.sort_values(['County', 'Year'], ascending=[True, False], inplace=True)
        
        # 使用執行緒池並行處理縣市統計資料
        futures = []
        for county in self.df['County'].unique():
            futures.append(
                self._executor.submit(self._compute_county_stats, county)
            )
        
        # 等待所有計算完成並儲存結果
        for future in futures:
            stats = future.result()
            self._stats_cache[stats.county] = stats
        
        # 快取常用資料
        self._years = sorted(self.df['Year'].unique(), reverse=True)
        self._available_counties = set(self.df['County'].unique())
            
    def _compute_county_stats(self, county: str) -> CountyStats:
        """
        計算單一縣市的統計資料
        
        Args:
            county: 縣市名稱
            
        Returns:
            CountyStats: 縣市統計資料物件
        """
        county_data = self.df[self.df['County'] == county]
        return CountyStats(
            county=county,
            years=county_data['Year'].values,
            registrations=county_data['Registrations'].values,
            deregistrations=county_data['Deregistrations'].values,
            neutered=county_data['Neutered'].values,
            neutering_rates=county_data['Neutering Rate'].values
        )
    
    @property
    def years(self) -> List[int]:
        """
        取得年份列表
        
        Returns:
            List[int]: 排序後的年份列表
        """
        return self._years
    
    @property
    def counties(self) -> List[str]:
        """
        取得依照指定順序排序的縣市列表
        
        Returns:
            List[str]: 依照指定順序排序的縣市列表
        """
        return [county for county in self._county_order if county in self._available_counties]
    
    @lru_cache(maxsize=32)
    def get_county_stats(self, county: str) -> Optional[CountyStats]:
        """
        取得縣市統計資料 (使用快取)
        
        Args:
            county: 縣市名稱
            
        Returns:
            Optional[CountyStats]: 縣市統計資料物件
        """
        return self._stats_cache.get(county)
    
    @lru_cache(maxsize=32)
    def get_county_data(self, county: str) -> List[Tuple]:
        """
        取得特定縣市的所有資料 (使用快取)
        
        Args:
            county: 縣市名稱
            
        Returns:
            List[Tuple]: 該縣市的所有年度資料
        """
        stats = self._stats_cache.get(county)
        return stats.records if stats else []
        
    def clear_cache(self):
        """清除所有快取資料"""
        with self._lock:
            self.get_county_data.cache_clear()
            self.get_county_stats.cache_clear()
            self._stats_cache.clear()
    
    def __del__(self):
        """解構時清理資源"""
        # 關閉執行緒池
        self._executor.shutdown(wait=True)
        # 清理快取
        self.clear_cache()