# %%
import pandas as pd
import numpy as np
# %%
df = pd.read_json('../data/price/aapl.json', convert_dates=True)
# %%
df.set_index('date', inplace=True)
df = df.sort_index(ascending=True)
# %%
data = pd.DataFrame(df['close'])
# %%
data

# %%
data.rename(columns={'close': 'price'}, inplace=True)
# %%
data['SMA1'] = data['price'].rolling(42).mean()
data
# %%
data['SMA2'] = data['price'].rolling(252).mean()
# %%
data.plot(title='AAPL | 42 & 252 days SMAs',figsize=(10, 6))
# %%
data['position'] = np.where(data['SMA1'] > data['SMA2'],1,-1)
# %%
data.dropna(inplace=True)
data
# %%
data['position'].value_counts()
# %%
data['returns'] = np.log(data['price'] / data['price'].shift(1))
# %%
data['strategy'] = data['position'].shift(1) * data['returns']
# %%
data[['returns', 'strategy']].sum()
# %%
data['returns'].sum()
# %%
data