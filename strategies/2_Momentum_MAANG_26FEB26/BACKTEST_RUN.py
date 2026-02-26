# %%
from BACKTESTER_CLASS import MomentumBacktester
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
momentum = 3

logger.info(f"Generating backtests for dates between {start} and {end} for {stocks}. Momentum: {momentum} days")
# %%
for ticker in stocks:
    momentum_maang_3d = MomentumBacktester(ticker,start, end, momentum, 10, 0.0)
    strategy_returns = momentum_maang_3d.run_strategy()
    hyper_param_str = f"{momentum}d"
    save_results(ticker, start, end, hyper_param_str, momentum_maang_3d.results)
    momentum_maang_3d.plot_results()
    logger.info(f"{ticker}:{strategy_returns}")
    

# %%
