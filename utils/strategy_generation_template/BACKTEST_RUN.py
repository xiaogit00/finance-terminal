# %%
from BACKTESTER_CLASS import xxx
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

stocks = []
start = "" #2015-01-01
end = ""

logger.info(f"Generating backtests for dates between {start} and {end} for {stocks}")
# %%
for ticker in stocks:
    strategy_stock = xxx(ticker, 40, 200, start, end)
    strategy_returns = strategy_stock.run_strategy()
    save_results(ticker, start, end, strategy_stock.results)
    logger.info(f"{ticker}:{strategy_returns}")
    

# %%
