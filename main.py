'''
脚本名称: 基于高低点分型的趋势策略

参考文章: https://zhuanlan.zhihu.com/p/56813297
'''

import pandas as pd
import mplfinance as mpf
import numpy as np
import matplotlib.patches as patches

def find_fractal(s: pd.Series, method : str = 'high'):
    '''
    找到分型点
    :param s: pd.Series
    :param method: str
    :return: pd.Series
    '''
    s = s.dropna()
    if method == 'high':
        high = (s.shift(1) < s) & (s.shift(-1) < s)
        ret = pd.Series(np.where(high, s, np.nan), index=s.index)
    elif method == 'low':
        low = (s.shift(1) > s) & (s.shift(-1) > s)
        ret = pd.Series(np.where(low, s, np.nan), index=s.index)
    return ret.dropna()

# 从data目录下读取SH000300.csv文件，日期列作为索引
df = pd.read_csv('data/SH000300.csv', index_col='日期', parse_dates=True)

df = df.rename(columns={'开盘': 'Open', '最高': 'High', '最低': 'Low', '收盘': 'Close'})

# 计算分型点
df['H1'] = find_fractal(df['Close'], method='high')
df['H2'] = find_fractal(df['H1'], method='high')
df['H3'] = find_fractal(df['H2'], method='high')
df['H4'] = find_fractal(df['H3'], method='high')
df['L1'] = find_fractal(df['Close'], method='low')
df['L2'] = find_fractal(df['L1'], method='low')
df['L3'] = find_fractal(df['L2'], method='low')
df['L4'] = find_fractal(df['L3'], method='low')

# 创建一个新的样式，上涨的K线为红色，下跌的K线为绿色
mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)

# 我们可以使用zip和tolist将其转化为坐标列表
G3_coords = list(zip(df['H3'].dropna().index.tolist(), df['H3'].dropna().values.tolist()))
L3_coords = list(zip(df['L3'].dropna().index.tolist(), df['L3'].dropna().values.tolist()))

# 为了满足alines的格式，我们将每个坐标点成对组合，形成线段
alines = [G3_coords, L3_coords]

apd = mpf.make_addplot(df['H3'],type='scatter')

# 绘制K线图
fig, axes = mpf.plot(df, type='candle', style=s, returnfig=True, alines=dict(alines=alines), addplot=apd)

# 对于每一个G1High的位置，添加一个红色的矩形框
for i in range(1, len(df) - 1):
    if df['H1'].iloc[i]:
        # 如果H1为NaN，则跳过
        if np.isnan(df['H1'].iloc[i]):
            continue

        # 计算矩形框的位置和大小
        low = min(df['Low'].iloc[i - 1:i + 1])
        high = max(df['High'].iloc[i - 1:i + 1])
        rect = patches.Rectangle((i - 1, low), 2, high - low, linewidth=1, edgecolor='r', facecolor='none')
        
        # 添加矩形框到图中
        axes[0].add_patch(rect)

# 对于每一个L1Low的位置，添加一个绿色的矩形框
for i in range(1, len(df) - 1):
    if df['L1'].iloc[i]:
        # 如果L1为NaN，则跳过
        if np.isnan(df['L1'].iloc[i]):
            continue

        # 计算矩形框的位置和大小
        low = min(df['Low'].iloc[i - 1:i + 1])
        high = max(df['High'].iloc[i - 1:i + 1])
        rect = patches.Rectangle((i - 1, low), 2, high - low, linewidth=1, edgecolor='g', facecolor='none')
        
        # 添加矩形框到图中
        axes[0].add_patch(rect)


# 显示图
mpf.show()