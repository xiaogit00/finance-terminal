# %%
from BACKTESTER_CLASS import MeanReversionBacktester
import sys
############## THE BELOW IS FOR MAKING IMPORTS CORRECT FOR LOGGING ################
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))
filename_without_ext = Path(__file__).stem
print(filename_without_ext)
from utils.logging_config import setup_logger
from utils.save_results import save_results
logger = setup_logger(filename_without_ext)
##############################

stocks = ["META", "AAPL", "AMZN", "NFLX", "GOOG"]
start = "2015-01-01"
end = "2019-12-31"
SMA = 30 
threshold = 2.5
logger.info(f"Generating backtests for dates between {start} and {end} for {stocks}")
# %%
for ticker in stocks:
    strategy_stock = MeanReversionBacktester(ticker, start, end, SMA, threshold, 1, 0.0)
    strategy_returns = strategy_stock.run_strategy()
    hyper_param_str = f'{SMA}SMA_{threshold}threshold'
    save_results(ticker, start, end, hyper_param_str, strategy_stock.results)
    strategy_stock.plot_results()
    logger.info(f"{ticker}:{strategy_returns}")
    

# %%
