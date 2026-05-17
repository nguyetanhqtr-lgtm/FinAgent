import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
df = pd.read_excel(r"C:\Users\LENOVO\Downloads\cleaned_data_updated.xlsx")
df['Date'] = pd.to_datetime(df['Date'])

# Chọn stock muốn vẽ
ticker = "AAPL"

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    row_heights=[0.7, 0.3],
    subplot_titles=(f"{ticker} Price Trend", "Volume")
)

# Panel trên: giá + MA7 + MA30
fig.add_trace(go.Scatter(
    x=df['Date'], y=df[f'{ticker}_Close'],
    name='Close Price', line=dict(color='blue', width=1.5)
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=df['Date'], y=df[f'{ticker}_MA7'],
    name='MA7', line=dict(color='orange', width=1, dash='dash')
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=df['Date'], y=df[f'{ticker}_MA30'],
    name='MA30', line=dict(color='red', width=1, dash='dash')
), row=1, col=1)

# Panel dưới: Volume
fig.add_trace(go.Bar(
    x=df['Date'], y=df[f'{ticker}_Volume'],
    name='Volume', marker_color='lightblue'
), row=2, col=1)

fig.update_layout(
    title=f"{ticker} Price Trend with Volume Overlay (2023-2024)",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    yaxis2_title="Volume",
    height=600,
    template="plotly_white"
)

fig.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Lấy tất cả cột return kể cả macro
return_cols = [col for col in df.columns if col.endswith('_return')]
returns_df = df[return_cols]

returns_df.columns = [
    col.replace('_return', '')
    for col in return_cols
]
# Tính correlation
corr = returns_df.corr()

# Vẽ heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    corr,
    annot=True,
    fmt='.2f',
    cmap='RdYlGn',
    center=0,
    vmin=-1, vmax=1,
    linewidths=0.5
)
plt.title('Correlation Heatmap of Daily Returns (2023-2024)', fontsize=14)
plt.tight_layout()
plt.show()

import plotly.figure_factory as ff
import numpy as np

# 4 stocks đại diện
stocks = ['NVDA', 'TSLA', 'JNJ', 'JPM']
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

# Lấy data return, bỏ NaN
data_kde = [df[f'{s}_return'].dropna().tolist() for s in stocks]

# Vẽ KDE
fig = ff.create_distplot(
    data_kde,
    group_labels=stocks,
    colors=colors,
    show_hist=False,
    show_rug=False
)

# Thêm đường dọc tại 0
fig.add_vline(x=0, line_dash='dash', line_color='gray', opacity=0.7)

fig.update_layout(
    title='Distribution of Daily Returns - KDE (2023-2024)',
    xaxis_title='Daily Return',
    yaxis_title='Density',
    template='plotly_white',
    height=500
)

fig.show()

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_excel(r"C:\Users\LENOVO\Downloads\cleaned_data.xlsx")
df['Date'] = pd.to_datetime(df['Date'])

# Tính Bollinger Bands cho NVDA
ticker = 'NVDA'
df['BB_std'] = df['NVDA_Close'].rolling(30).std()
df['BB_upper'] = df['NVDA_MA30'] + 2 * df['BB_std']
df['BB_lower'] = df['NVDA_MA30'] - 2 * df['BB_std']

fig = go.Figure()

# Bollinger Bands (vùng tô màu)
fig.add_trace(go.Scatter(
    x=df['Date'], y=df['BB_upper'],
    name='BB Upper', line=dict(color='rgba(0,100,255,0.5)', width=1),
    fill=None
))
fig.add_trace(go.Scatter(
    x=df['Date'], y=df['BB_lower'],
    name='BB Lower', line=dict(color='rgba(0,100,255,0.5)', width=1),
    fill='tonexty', fillcolor='rgba(0,100,255,0.1)'
))

# Giá + MA7 + MA30
fig.add_trace(go.Scatter(
    x=df['Date'], y=df[f'{ticker}_Close'],
    name='Close Price', line=dict(color='blue', width=1.5)
))
fig.add_trace(go.Scatter(
    x=df['Date'], y=df[f'{ticker}_MA7'],
    name='MA7', line=dict(color='orange', width=1, dash='dash')
))
fig.add_trace(go.Scatter(
    x=df['Date'], y=df[f'{ticker}_MA30'],
    name='MA30', line=dict(color='red', width=1, dash='dash')
))

fig.update_layout(
    title=f'{ticker} Rolling Statistics with Bollinger Bands (2023-2024)',
    xaxis_title='Date',
    yaxis_title='Price (USD)',
    template='plotly_white',
    height=550
)

fig.show()