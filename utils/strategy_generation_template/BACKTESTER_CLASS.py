import numpy as np
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

class SampleBacktesterClass(object):
    ''' To backtest for a particular ticker, simply instantiate and call methods.

        Attributes
        ==========
        symbol: str
            RIC symbol with which to work
        indicator1: int
            time window in days for shorter SMA
        indicator1: int
            time window in days for longer SMA
        start: str
            start date for data retrieval
        end: str
            end date for data retrieval

        Methods
        =======
        set_parameters:
            sets one or two new SMA parameters
        run_strategy:
            runs the backtest for the SMA-based strategy
        plot_results:
            plots the performance of the strategy compared to the symbol
        update_and_run:
            updates SMA parameters and returns the (negative) absolute performance
        optimize_parameters:
            implements a brute force optimization for the two SMA parameters

        Examples:
        ========
        import SMAVectorBacktester as SMA
        smabt = SMA.SMAVectorBacktester('EUR=', 42, 252, '2010-1-1', '2019-12-31')
        smabt.run_strategy() -> (1.29, 0.45)
        smabt.optimize_parameters((30, 50, 2),(200, 300, 2)) -> (array([ 48., 238.]), 1.5)
        smabt.plot_results()
    '''

    def __init__(self, symbol, indicator1, indicator, start, end):
        self.symbol = symbol
        self.indicator1 = indicator1
        self.indicator = indicator
        self.start = start
        self.end = end
        self.results = None
        self.get_data(symbol)
    
    def get_data(self, symbol):
        ''' Retrieves and prepares the data.
        '''
        df = pd.read_csv(
            f'../../data/price/{symbol}_full.csv',
            header=0,
            skiprows=[1, 2]
        ).rename(columns={"Price": "Date", "Close": "price"}).set_index(keys='Date')
        df.index = pd.to_datetime(df.index)
        df = df.loc[self.start:self.end]
        df2 = pd.DataFrame(df['price']) # Retain only the close price column
        # print(df2)
        df2['return'] = np.log(df2 / df2.shift(1))
        df2['SMA1'] = df['price'].rolling(self.SMA1).mean()
        df2['SMA2'] = df['price'].rolling(self.SMA2).mean()
        self.data = df2


    def run_strategy(self):
        ''' Backtests the trading strategy.
        '''
        data = self.data.copy().dropna()
        data['position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
        data['strategy'] = data['position'].shift(1) * data['return']
        data.dropna(inplace=True)
        data['benchmark_returns'] = data['return'].cumsum().apply(np.exp)
        data['strategy_returns'] = data['strategy'].cumsum().apply(np.exp)
        self.results = data
        # gross performance of the strategy
        strategy_returns = data['strategy_returns'].iloc[-1].item() # Last row of strategy returns - the actual returns
        benchmark_returns = data['benchmark_returns'].iloc[-1].item()
        difference_in_returns = strategy_returns - benchmark_returns
        return {
            "strategy_returns": round(strategy_returns, 2),
            "benchmark_returns": round(benchmark_returns, 2),
            "difference_in_returns": round(difference_in_returns, 2),
        }
    def plot_results(self):
        ''' Plots the cumulative performance of the trading strategy
        compared to the symbol.
        '''
        if self.results is None:
            print('No results to plot yet. Run a strategy.')
        save_dir = "backtest_charts"
        os.makedirs(save_dir, exist_ok=True)
        title = 'StrategyName %s | %sd hyperParamX | TC = %.2f' % (self.symbol, self.hyperParam, self.tc)
        ax = self.results[['benchmark_returns', 'strategy_returns']].plot(
                title=title,
                figsize=(10, 6)
            )
        
        run_id = datetime.now().strftime("%d%b%y").upper()
        file_path = os.path.join(save_dir, f"{self.start}_to_{self.end}_{self.symbol}_momentum{self.momentum}d_{run_id}.png")
        # Save figure
        fig = ax.get_figure()
        fig.savefig(file_path, bbox_inches="tight", dpi=300)
        plt.show()
        plt.close(fig)  # Prevent memory buildup if running many plots

        print(f"Plot saved to {file_path}")

