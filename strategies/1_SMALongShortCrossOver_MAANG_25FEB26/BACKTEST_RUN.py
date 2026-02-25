# %%
from BACKTESTER_CLASS import SMACrossoverStrategyBacktester
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
print(PROJECT_ROOT)
sys.path.append(str(PROJECT_ROOT))
filename_without_ext = Path(__file__).stem
print(filename_without_ext)
from utils.logging_config import setup_logger
from utils.save_results import save_results

logger = setup_logger(filename_without_ext)
stocks = ["META", "AAPL", "AMZN", "NFLX", "GOOG"]
start = "2015-01-01"
end = "2019-12-31"

logger.info(f"Generating backtests for dates between {start} and {end} for {stocks}")
# %%
for ticker in stocks:
    sma_crossover_stock = SMACrossoverStrategyBacktester(ticker, 40, 200, start, end)
    strategy_returns = sma_crossover_stock.run_strategy()
    save_results(ticker, start, end, sma_crossover_stock.results)
    logger.info(f"{ticker}:{strategy_returns}")
    

# %%
