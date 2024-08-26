# -*- coding: utf-8 -*-
"""
讀取 TOF-MS 原始資料後繪圖；共有「三個滑桿」，以及隨滑桿調整而變動的「三個圖表」。

- 滑桿分別控制：
    1. 時間錨 (time anchor)
    2. 縮放 (zoom)
    3. 訊雜比 (signal ratio)
- 圖表分別為：
    1. 無標註的原始圖 (使用 `plt.plot()`)
    2. 只包含訊號的無標註圖 (使用 `plt.bar()`)
    3. 標記了雜混基線、區間，以及訊號範圍的圖

---

After reading the TOF-MS raw data, the graph is drawn; there are "three sliders" and "three charts" that change with the adjustment of the sliders.

- Sliders control respectively:
    1. time anchor
    2. zoom
    3. Signal ratio
- The charts are:
    1. Unlabeled original figure (using `plt.plot()`)
    2. Unlabeled plot containing only signals (use `plt.bar()`)
    3. Graph with labeled clutter baseline, interval, and signal range
"""
import os
import time
from collections import Counter

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def main():
    # 取得 "./MS_data/" 資料夾下的所有檔案名稱
    file_list = ["./MS_data/" + file for file in os.listdir("./MS_data/")]
    
    # 建立 "./outputs_當前時間/" 資料夾
    local_time = time.strftime("%Y%m%d_%H%M%S")
    output_dir = "./outputs_" + local_time + "/"
    os.makedirs(output_dir)

    # 對於每個 MS_data 檔案
    for file in file_list:

        # 讀取檔案
        data = pd.read_csv(file, sep=' ', header=None)

        # 指定 column names
        data.columns = ['micro_sec', 'mini_volts']

        # 排版
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
        plt.subplots_adjust(left=0.1, bottom=0.3)
        fig.suptitle(f'{file.split("/")[-1]}')

        # 設置滑桿位置
        ax_time_anchor_slider = plt.axes([0.1, 0.25, 0.8, 0.02])
        ax_zoom_slider = plt.axes([0.1, 0.15, 0.8, 0.02])
        ax_signal_ratio_slider = plt.axes([0.1, 0.05, 0.8, 0.02])

        # 創建滑桿
        time_anchor_slider = Slider(ax_time_anchor_slider, 'Time anchor', data['micro_sec'].min(), data['micro_sec'].max(), valinit=data['micro_sec'].min(), valstep=0.00025)
        zoom_slider = Slider(ax_zoom_slider, 'Zoom', 0.00125, data['micro_sec'].max(), valinit=data['micro_sec'].max(), valstep=0.00025)
        signal_ratio_slider = Slider(ax_signal_ratio_slider, 'SNR', 0.01, 1, valinit=0.6, valstep=0.01)

        # (1) 無標註的原始圖
        ax1.plot(data['micro_sec'], data['mini_volts'], lw=1)
        ax1.set_title('Unlabeled')

        # (2) 只包含訊號的無標註圖
        ax2.bar(data['micro_sec'], data['mini_volts'], width=0.2)
        ax2.set_title('Signals')

        # (3) 標記了雜混基線、區間，以及訊號範圍的圖
        ax3.plot(data['micro_sec'], data['mini_volts'], lw=1)
        ax3.axhline(y=data['mini_volts'].mode().iloc[0], color='red', linestyle='--')  # baseline
        ax3.set_title('labeled noise Baseline, Threshold & Signal')

        # 更新時間錨及縮放的函數
        def update(val):
            time_anchor = time_anchor_slider.val
            zoom = zoom_slider.val
            sr = signal_ratio_slider.val
            
            # 更新原始圖
            ax1.set_xlim(time_anchor - zoom/2, time_anchor + zoom/2)
            
            # 更新只包含訊號的圖
            ax2.set_xlim(time_anchor - zoom/2, time_anchor + zoom/2)
            
            # 更新標記圖
            ax3.set_xlim(time_anchor - zoom/2, time_anchor + zoom/2)

            fig.canvas.draw_idle()

        # 更新 signal_ratio 的函數
        def update_2(val):
            time_anchor = time_anchor_slider.val
            zoom = zoom_slider.val
            sr = signal_ratio_slider.val
            
            # 更新原始圖
            ax1.set_xlim(time_anchor - zoom/2, time_anchor + zoom/2)
            
            # 更新只包含訊號的圖
            ax2.set_xlim(time_anchor - zoom/2, time_anchor + zoom/2)
            
            # 更新標記圖
            ax3.set_xlim(time_anchor - zoom/2, time_anchor + zoom/2)

            # 根據 signal ratio 計算 max_noise
            max_noise = data['mini_volts'].max() - (data['mini_volts'].max() - data['mini_volts'].mode().iloc[0]) * sr
            ax3.axhline(y=max_noise, color='#FE9900', linestyle='--')  # max_noise line

            # 對於每個時間點
            for i, time in enumerate(data['micro_sec']):
            # 判斷是否為信號，若是則標記時間點
                if data['mini_volts'].iloc[i] > max_noise:
                    ax3.plot(time, data['mini_volts'].iloc[i], marker='*', color='red', markersize=10)

            fig.canvas.draw_idle()

        # 設置滑桿的更新事件
        time_anchor_slider.on_changed(update)
        zoom_slider.on_changed(update)
        signal_ratio_slider.on_changed(update_2)

        plt.show()

        # 按 Enter 後儲存圖表
        plt.savefig(output_dir + file.split("/")[-1].replace(".data", ".png"))
        




main()