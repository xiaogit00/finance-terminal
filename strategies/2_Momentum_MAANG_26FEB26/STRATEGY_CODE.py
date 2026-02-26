def run_strategy(self, momentum=1):
    ''' Backtests the trading strategy.
    '''
    self.momentum = momentum
    data = self.data.copy().dropna()
    data['position'] = np.sign(data['return'].rolling(momentum).mean())
    data['strategy'] = data['position'].shift(1) * data['return']
    # determine when a trade takes place
    data.dropna(inplace=True)
    trades = data['position'].diff().fillna(0) != 0
    # subtract transaction costs from return when trade takes place
    data['strategy'][trades] -= self.tc
    data['benchmark_returns'] = self.amount * data['return'].cumsum().apply(np.exp)
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