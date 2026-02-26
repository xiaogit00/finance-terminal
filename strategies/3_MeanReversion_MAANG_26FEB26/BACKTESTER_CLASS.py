import numpy as np
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

class MeanReversionBacktester(object):
    ''' To backtest for a particular ticker, simply instantiate and call methods.

        Attributes
        ==========
        symbol: str
            RIC symbol with which to work
        start: str
            start date for data retrieval
        end: str
            end date for data retrieval
        SMA: int
            the number of previous returns for SMA calculation
        threshold: int
            the distance threshold beyond which it indicates a large deviation from 'mean'/SMA
        amount: int, float
            amount to be invested at the beginning
        tc: float
            proportional transaction costs (e.g., 0.5% = 0.005) per trade

        Methods
        =======
        set_parameters:
            sets one or two new SMA parameters
        run_strategy:
            runs the backtest for the SMA-based strategy
        plot_results:
            plots the performance of the strategy compared to the symbol


        Examples:
        ========
        Examples:
        ========
        import MomentumBacktester 
        aapl_meanReversion_30d = MomentumBacktester('AAPL', '2010-1-1','2019-12-31', 10, 0.0)
        aapl_meanReversion_30d.run_strategy(momentum=3)
        aapl_meanReversion_30d.plot_results()
    '''

    def __init__(self, symbol, start, end, SMA, threshold, amount, tc):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.SMA = SMA
        self.threshold = threshold
        self.amount = amount
        self.tc = tc
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
        self.data = df2


    def run_strategy(self):
        ''' Backtests the trading strategy.
        '''
        data = self.data.copy().dropna()
        data['sma'] = data['price'].rolling(self.SMA).mean()
        data['distance'] = data['price'] - data['sma']
        data.dropna(inplace=True)
        # sell signals
        data['position'] = np.where(data['distance'] > self.threshold, -1, np.nan)
        # buy signals
        data['position'] = np.where(data['distance'] < -self.threshold, 1, data['position'])
        # crossing of current price and SMA (zero distance)
        data['position'] = np.where(data['distance'] *
        data['distance'].shift(1) < 0, 0, data['position'])
        data['position'] = data['position'].ffill().fillna(0)
        data['strategy'] = data['position'].shift(1) * data['return']
        # determine when a trade takes place
        trades = data['position'].diff().fillna(0) != 0
        # subtract transaction costs from return when trade takes place
        data['strategy'][trades] -= self.tc
        data['benchmark_returns'] = self.amount *  data['return'].cumsum().apply(np.exp)
        data['strategy_returns'] = self.amount * data['strategy'].cumsum().apply(np.exp)
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
        title = 'Mean Reversion %s | %sd SMA | %s threshold |TC = %.2f' % (self.symbol, self.SMA, self.threshold,self.tc)
        ax = self.results[['benchmark_returns', 'strategy_returns']].plot(
                title=title,
                figsize=(10, 6)
            )
        
        run_id = datetime.now().strftime("%d%b%y").upper()
        file_path = os.path.join(save_dir, f"{self.start}_to_{self.end}_{self.symbol}_SMA{self.SMA}d_{self.threshold}threshold_{run_id}.png")
        # Save figure
        fig = ax.get_figure()
        fig.savefig(file_path, bbox_inches="tight", dpi=300)
        plt.show()
        plt.close(fig)  # Prevent memory buildup if running many plots

        print(f"Plot saved to {file_path}")

