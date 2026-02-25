def run_strategy(self):
    ''' Backtests the trading strategy.
    '''
    data = self.data.copy().dropna()
    data['position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
    data['strategy'] = data['position'].shift(1) * data['return']
    data.dropna(inplace=True)
    data['creturns'] = data['return'].cumsum().apply(np.exp)
    data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)
    self.results = data
    # gross performance of the strategy
    strategy_returns = data['cstrategy'].iloc[-1].item() # Last row of strategy returns - the actual returns
    benchmark_returns = data['creturns'].iloc[-1].item()
    difference_in_returns = strategy_returns - benchmark_returns
    return {
        "strategy_returns": round(strategy_returns, 2),
        "benchmark_returns": round(benchmark_returns, 2),
        "difference_in_returns": round(difference_in_returns, 2),
    }