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
"""
import os
import time
# from collections import Counter

import numpy as np
import pandas as pd
# from pandas import Series, DataFrame

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


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

        # 排版 & 繪圖
        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.1, bottom=0.25)
        fig.suptitle(f'{file.split("/")[-1]}')

        ax.plot(data['micro_sec'], data['mini_volts'], lw=1)
        ax.axhline(y=data['mini_volts'].mode().iloc[0], color='red')  # baseline

        # 設置滑桿位置
        ax_time_anchor_slider = plt.axes([0.1, 0.11, 0.8, 0.01])
        ax_zoom_slider = plt.axes([0.1, 0.06, 0.8, 0.01])
        ax_signal_ratio_slider = plt.axes([0.1, 0.01, 0.8, 0.01])

        # 創建滑桿
        time_anchor_slider = Slider(ax_time_anchor_slider, 'Time anchor', data['micro_sec'].min(), data['micro_sec'].max(), valinit=data['micro_sec'].max()/2, valstep=0.00025)
        zoom_slider = Slider(ax_zoom_slider, 'Zoom', 0.00125, data['micro_sec'].max(), valinit=data['micro_sec'].max(), valstep=0.00025)
        signal_ratio_slider = Slider(ax_signal_ratio_slider, 'Signal ratio', 0.01, 1, valinit=0.95, valstep=0.01)

        # 設定按鈕位置
        ax_button1 = plt.axes([0.1, 0.16, 0.07, 0.03])
        ax_button2 = plt.axes([0.2, 0.16, 0.07, 0.03])
        ax_button3 = plt.axes([0.3, 0.16, 0.07, 0.03])
        ax_button4 = plt.axes([0.4, 0.16, 0.07, 0.03])
        ax_button5 = plt.axes([0.5, 0.16, 0.07, 0.03])
        
        # 創建按鈕
        button1 = Button(ax_button1, 'Original')
        button2 = Button(ax_button2, 'Signals')
        button3 = Button(ax_button3, 'Labeled')
        button4 = Button(ax_button4, 'Save & Next')
        button5 = Button(ax_button5, 'annotate')

        # 設定按鈕回調函數
        def show_original(event):
            global signal_bars_state
            signal_bars_state = False
            ax.clear()
            ax.plot(data['micro_sec'], data['mini_volts'], lw=1)
            ax.set_title('Unlabeled')
            signal_ratio_slider.ax.set_visible(True)
            fig.canvas.draw_idle()

        def show_signals(event):
            sr = signal_ratio_slider.val
            global signal_bars_state
            signal_bars_state = True

            ax.clear()
            max_noise = data['mini_volts'].max() - (data['mini_volts'].max() - data['mini_volts'].mode().iloc[0]) * sr
            # 繪製垂直線
            for x, y in zip(data[data['mini_volts'] > max_noise]['micro_sec'], data[data['mini_volts'] > max_noise]['mini_volts']):
                signal_bar = ax.plot([x, x], [0, y], lw=1, color='#1c8acd')

            ax.set_xlim(time_anchor_slider.val - zoom_slider.val/2, time_anchor_slider.val + zoom_slider.val/2)
            ax.set_title('Signals')
            signal_ratio_slider.ax.set_visible(True)
            fig.canvas.draw_idle()

        def show_labeled(event):
            global signal_bars_state
            signal_bars_state = False
            ax.clear()
            ax.plot(data['micro_sec'], data['mini_volts'], lw=1)
            ax.axhline(y=data['mini_volts'].mode().iloc[0], color='red')  # baseline
            ax.set_title('Labeled')
            signal_ratio_slider.ax.set_visible(True)
            fig.canvas.draw_idle()

        def save_and_next(event):
            plt.savefig(output_dir + file.split("/")[-1].replace(".data", ".png"))
            plt.close()
            next
        def annotate(event):
            sr = signal_ratio_slider.val

            global annotations

            # 初始化 annotations
            if 'annotations' not in globals():
                annotations = []

            # 移除現有的註解
            if annotations:
                for annotation in annotations:
                    annotation.remove()
                annotations = []
            else:
                max_noise = data['mini_volts'].max() - (data['mini_volts'].max() - data['mini_volts'].mode().iloc[0]) * sr
                
                # 標註座標
                for x, y in zip(data[data['mini_volts'] > max_noise]['micro_sec'], data[data['mini_volts'] > max_noise]['mini_volts']):
                    annotation = ax.annotate(f'({x:.2f}, {y:.2f})', xy=(x, y), xytext=(5, 5), textcoords='offset points', fontsize=8, color='blue')
                    annotations.append(annotation)

            fig.canvas.draw_idle()

        # 設定按鈕更新事件
        button1.on_clicked(show_original)
        button2.on_clicked(show_signals)
        button3.on_clicked(show_labeled)
        button4.on_clicked(save_and_next)
        button5.on_clicked(annotate)

        # 更新時間錨及縮放的函數
        def update(val):
            time_anchor = time_anchor_slider.val
            zoom = zoom_slider.val
            
            # 更新圖表
            ax.set_xlim(time_anchor - zoom/2, time_anchor + zoom/2)
            fig.canvas.draw_idle()

        # 更新 signal_ratio 的函數
        def update_2(val):
            global max_noise_line
            global stars            

            if 'max_noise_line' in globals():
                max_noise_line.remove()
            
            if 'stars' in globals():
                for star in stars:
                    star.remove()

            time_anchor = time_anchor_slider.val
            zoom = zoom_slider.val
            sr = signal_ratio_slider.val
            
            # 更新圖表
            ax.set_xlim(time_anchor - zoom/2, time_anchor + zoom/2)
            max_noise = data['mini_volts'].max() - (data['mini_volts'].max() - data['mini_volts'].mode().iloc[0]) * sr
            max_noise_line = ax.axhline(y=max_noise, color='red', linestyle='--')  # max_noise line
            stars = ax.plot(data[data['mini_volts'] > max_noise]['micro_sec'], data[data['mini_volts'] > max_noise]['mini_volts'], marker='*', color='red', linestyle='')
            
            if signal_bars_state:
                show_signals(None)

            fig.canvas.draw_idle()

        # 設定滑桿的更新事件
        time_anchor_slider.on_changed(update)
        zoom_slider.on_changed(update)
        signal_ratio_slider.on_changed(update_2)

        plt.show()

main()