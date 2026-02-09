# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('seaborn-v0_8')
# %%
df = pd.read_csv('../data/price/AAPL_full.csv', header=0,
            skiprows=[1, 2])
# %%
df
# %%
df.set_index('Price', inplace=True)
df = df.sort_index(ascending=True)
# %%
data = pd.DataFrame(df['Close'])
# %%
data = data.loc['2021-01-01': '2022-06-01']
data

# %%
data.rename(columns={'close': 'price'}, inplace=True)
# %%
np.exp(np.log(data['Close'] / data['Close'].shift(1)).sum())
# %%
data['SMA1'] = data['price'].rolling(42).mean()
data
# %%
data['SMA2'] = data['price'].rolling(252).mean()
# %%
data.dropna(inplace=True)
data
# %%
data.plot(title='AAPL | 42 & 252 days SMAs',figsize=(10, 6))
# %%
data['position'] = np.where(data['SMA1'] > data['SMA2'],1,-1)
data.dropna(inplace=True)
# %%
data['position'].value_counts()
# %%
data['returns'] = np.log(data['price'] / data['price'].shift(1))
# %%
data['strategy'] = data['position'].shift(1) * data['returns']
# %%
data[['returns', 'strategy']].sum().apply(np.exp)
# %%
data[['returns', 'strategy']].cumsum().apply(np.exp).plot(figsize=(10, 6))
# %%
data[['returns', 'strategy']].cumsum().apply(np.exp)

# %%

fig, ax1 = plt.subplots(figsize=(10, 6))

# --- Plot cumulative returns on left axis ---
(data[['returns', 'strategy']]
 .cumsum()
 .apply(np.exp)
 .plot(ax=ax1))

ax1.set_ylabel("Cumulative Returns")
ax1.set_title("Strategy Performance with Market Positioning")

# --- Plot position on right axis ---
ax2 = ax1.twinx()
data['position'].plot(
    ax=ax2,
    color='black',
    alpha=0.3,
    ylim=[-1.1, 1.1],
    label='Position'
)

ax2.set_ylabel("Position")

# Optional: legend handling
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()

# %%
import matplotlib.pyplot as plt
import numpy as np

fig, ax1 = plt.subplots(figsize=(10, 6))

# --- 1. Price + SMAs (main axis) ---
data.plot(
    ax=ax1,
    title='AAPL | Price, SMAs, Strategy & Position',
)
ax1.set_ylabel("Price")

# --- 2. Cumulative returns (2nd axis) ---
ax2 = ax1.twinx()

(data[['returns', 'strategy']]
 .cumsum()
 .apply(np.exp)
 .plot(
     ax=ax2,
     linestyle='--',
     alpha=0.7
 ))

ax2.set_ylabel("Cumulative Returns")

# --- 3. Position (3rd axis, offset) ---
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('axes', 1.1))  # push axis outward

data['position'].plot(
    ax=ax3,
    color='black',
    alpha=0.3,
    ylim=[-1.1, 1.1],
    label='Position'
)

ax3.set_ylabel("Position")

# --- Legends (manual but clean) ---
lines, labels = [], []

for ax in [ax1, ax2, ax3]:
    l, lab = ax.get_legend_handles_labels()
    lines.extend(l)
    labels.extend(lab)

ax1.legend(lines, labels, loc='upper left')

plt.show()

