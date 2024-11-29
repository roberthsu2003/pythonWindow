import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Optional
import tkintermapview

class TaiwanMapRenderer(ttk.Frame):
    """台灣地圖渲染器,用於顯示和互動的地圖介面"""
    
    def __init__(self, master: tk.Widget, data_manager, height=400):
        """
        初始化地圖渲染器
        
        Args:
            master: 父層視窗
            data_manager: 資料管理器實例
            height: 地圖高度 (預設 400)
        """
        super().__init__(master)
        self.data_manager = data_manager
        self.on_county_select: Optional[Callable[[str], None]] = None
        
        # 初始化地圖元件
        self.map_widget = tkintermapview.TkinterMapView(self, width=400, height=height)
        self.map_widget.pack(fill="both", expand=True)
        
        # 使用國土測繪中心圖資
        self.map_widget.set_tile_server(
            "https://wmts.nlsc.gov.tw/wmts/EMAP/default/EPSG:3857/{z}/{y}/{x}",
            max_zoom=19
        )
        
        # 設定初始位置和縮放級別 (台灣中心點)
        self.map_widget.set_position(23.97565, 120.973882)
        self.map_widget.set_zoom(7)
        
        # 初始化標記相關屬性
        self.markers = {}
        self.selected_county = None
        self.selected_marker = None
        
        # 建立縣市標記
        self._create_markers()
        
    def _create_markers(self):
        """建立所有縣市的地圖標記"""
        # 定義縣市座標
        county_positions = {
            "臺北市": (25.033, 121.565),
            "新北市": (25.037, 121.437),
            "桃園市": (24.989, 121.313),
            "臺中市": (24.148, 120.674),
            "臺南市": (23.000, 120.227),
            "高雄市": (22.627, 120.301),
            "基隆市": (25.128, 121.742),
            "新竹市": (24.814, 120.968),
            "新竹縣": (24.839, 121.013),
            "苗栗縣": (24.560, 120.821),
            "彰化縣": (24.052, 120.516),
            "南投縣": (23.961, 120.988),
            "雲林縣": (23.709, 120.431),
            "嘉義市": (23.480, 120.449),
            "嘉義縣": (23.452, 120.256),
            "屏東縣": (22.552, 120.549),
            "宜蘭縣": (24.702, 121.738),
            "花蓮縣": (23.987, 121.601),
            "臺東縣": (22.797, 121.144),
            "澎湖縣": (23.571, 119.579),
            "金門縣": (24.449, 118.376),
            "連江縣": (26.151, 119.950)
        }

        # 為每個縣市建立標記
        for county, pos in county_positions.items():
            marker = self.map_widget.set_marker(
                pos[0], pos[1], 
                text=county,
                command=lambda c=county: self._on_marker_click(c)
            )
            self.markers[county] = marker

    def _on_marker_click(self, county: str):
        """
        處理標記點擊事件
        
        Args:
            county: 被點擊的縣市名稱
        """
        if self.on_county_select:
            self.on_county_select(county)

    def select_county(self, county_name: str):
        """
        選擇特定縣市
        
        Args:
            county_name: 縣市名稱
        """
        # 處理全臺的情況
        if county_name == "全臺":
            # 清除上一個選擇的標記
            if self.selected_marker:
                self.selected_marker.set_text(self.selected_county)
            
            # 重置選擇狀態
            self.selected_marker = None
            self.selected_county = None
            
            # 設定地圖顯示全臺灣的視角
            self.map_widget.set_position(23.97565, 120.973882)
            self.map_widget.set_zoom(7)
            return
        
        # 處理其他縣市的情況
        if county_name not in self.markers:
            return
            
        # 重設上一個選擇的標記
        if self.selected_marker:
            self.selected_marker.set_text(self.selected_county)
        
        # 設定新的選擇標記
        marker = self.markers[county_name]
        marker.set_text("🔴 " + county_name)
        
        # 移動地圖至選擇的縣市
        self.map_widget.set_position(
            marker.position[0], 
            marker.position[1]
        )
        self.map_widget.set_zoom(9)
        
        # 更新選擇狀態
        self.selected_county = county_name
        self.selected_marker = marker
    def clear_markers(self):
        """清除所有地圖標記"""
        try:
            # 安全地清除所有標記
            for marker in list(self.markers.values()):
                try:
                    if marker and hasattr(marker, 'delete'):
                        marker.delete()
                except Exception:
                    pass
            self.markers.clear()
        except Exception:
            pass

    def destroy(self):
        """清理資源"""
        try:
            # 清除標記
            self.clear_markers()
            
            # 清除地圖元件
            if hasattr(self, 'map_widget'):
                self.map_widget.destroy()
                
        except Exception:
            pass
            
        # 最後調用父類的destroy
        try:
            super().destroy()
        except Exception:
            pass