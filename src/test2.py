# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('seaborn-v0_8')

# %%
df = pd.read_csv('../data/price/NVDA_full.csv', header=0, skiprows=[1, 2])
# %%
df.set_index(keys='Price', inplace=True)
# %%
df.index = pd.to_datetime(df.index)

# %%
data = df.loc['2024-01-01':'2024-06-30']['Close']
# %%
data
# %%
data.std()
# %%
data.max()
# %%
data.min()
# %%
data.info