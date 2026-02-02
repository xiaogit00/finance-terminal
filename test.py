# %%
import pandas as pd
import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parents[1]))
from src.classes.SMAVectorBacktester import SMAVectorBacktester
%load_ext autoreload
%autoreload 2
# %%
bt = SMAVectorBacktester("MSFT", 42, 252, '2010-01-01', '2026-01-01')
# %%

bt.data
# %%
bt.run_strategy()
# %%
bt.results.tail()
# %%
bt.plot_results()
# %%
