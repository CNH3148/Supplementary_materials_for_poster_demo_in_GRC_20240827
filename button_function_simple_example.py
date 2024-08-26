import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# 創建圖表
fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [10, 20, 25, 30], lw=1)

# 創建按鈕
ax_button = plt.axes([0.7, 0.05, 0.1, 0.075])
button = Button(ax_button, 'annotate')

# 初始化註解列表
annotations = []

def annotate(event):
    global annotations

    # 移除現有的註解
    if annotations:
        for annotation in annotations:
            annotation.remove()
        annotations = []
    else:
        # 添加新的註解
        for x, y in zip([0, 1, 2, 3], [10, 20, 25, 30]):
            annotation = ax.annotate(f'({x}, {y})', xy=(x, y), xytext=(5, 5), textcoords='offset points', fontsize=8, color='blue')
            annotations.append(annotation)

    fig.canvas.draw_idle()

# 設定按鈕回調函數
button.on_clicked(annotate)

plt.show()
