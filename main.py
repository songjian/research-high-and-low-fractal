'''
脚本名称: 基于高低点分型的趋势策略

参考文章: https://zhuanlan.zhihu.com/p/56813297
'''

import pandas as pd
import mplfinance as mpf
import numpy as np
import matplotlib.patches as patches

# 从data目录下读取SH000300.csv文件，日期列作为索引
df = pd.read_csv('data/SH000300.csv', index_col='日期', parse_dates=True)

df = df.rename(columns={'开盘': 'Open', '最高': 'High', '最低': 'Low', '收盘': 'Close'})

# 单独保存收盘列
close = df['Close']

# 计算G1High，如果收盘价大于前一天的收盘价和后一天的收盘价，则为G1High，G1High为True，否则为False
G1High = (close.shift(1) < close) & (close.shift(-1) < close)

# 创建一个新列来存储G1High的值，如果G1High为True，那么这个新列的值就是收盘价，否则为np.nan
df['G1High'] = np.where(G1High, df['Close'], np.nan)

# 计算L1Low，如果收盘价小于前一天的收盘价和后一天的收盘价，则为L1Low，L1Low为True，否则为False
L1Low = (close.shift(1) > close) & (close.shift(-1) > close)

# 创建一个新列来存储L1Low的值，如果L1Low为True，那么这个新列的值就是收盘价，否则为np.nan
df['L1Low'] = np.where(L1Low, df['Close'], np.nan)

# 创建一个新的样式，上涨的K线为红色，下跌的K线为绿色
mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)

# 绘制K线图
fig, axes = mpf.plot(df, type='candle', style=s, returnfig=True)

# 对于每一个G1High的位置，添加一个红色的矩形框
for i in range(1, len(df) - 1):
    if G1High.iloc[i]:
        # 计算矩形框的位置和大小
        low = min(df['Low'].iloc[i - 1:i + 1])
        high = max(df['High'].iloc[i - 1:i + 1])
        rect = patches.Rectangle((i - 1, low), 2, high - low, linewidth=1, edgecolor='r', facecolor='none')
        
        # 添加矩形框到图中
        axes[0].add_patch(rect)

# 对于每一个L1Low的位置，添加一个绿色的矩形框
for i in range(1, len(df) - 1):
    if L1Low.iloc[i]:
        # 计算矩形框的位置和大小
        low = min(df['Low'].iloc[i - 1:i + 1])
        high = max(df['High'].iloc[i - 1:i + 1])
        rect = patches.Rectangle((i - 1, low), 2, high - low, linewidth=1, edgecolor='g', facecolor='none')
        
        # 添加矩形框到图中
        axes[0].add_patch(rect)

# 显示图
mpf.show()
