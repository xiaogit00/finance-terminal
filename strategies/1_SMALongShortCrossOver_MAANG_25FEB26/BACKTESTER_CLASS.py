import numpy as np
import pandas as pd
import os

class SMACrossoverStrategyBacktester(object):
    ''' To backtest for a particular ticker, simply instantiate and call methods.
    Class for the vectorized backtesting of SMA-based trading strategies. Assumes that you already have the data downloaded in data/prices folder.

        Attributes
        ==========
        symbol: str
            RIC symbol with which to work
        SMA1: int
            time window in days for shorter SMA
        SMA2: int
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

    def __init__(self, symbol, SMA1, SMA2, start, end):
        self.symbol = symbol
        self.SMA1 = SMA1
        self.SMA2 = SMA2
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

    def set_parameters(self, SMA1=None, SMA2=None):
        ''' Updates SMA parameters and resp. time series.
        '''
        if SMA1 is not None:
            self.SMA1 = SMA1
            self.data['SMA1'] = self.data['price'].rolling(self.SMA1).mean()
        if SMA2 is not None:
            self.SMA2 = SMA2
            self.data['SMA2'] = self.data['price'].rolling(self.SMA2).mean()

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
        title = 'SMALongShort: %s | SMA1=%d, SMA2=%d' % (self.symbol,
                                            self.SMA1, self.SMA2)
        self.results[['benchmark_returns', 'strategy_returns']].plot(title=title,
                                                    figsize=(10, 6))
