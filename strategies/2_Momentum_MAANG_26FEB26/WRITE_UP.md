# General idea of Momentum strategy
Simple form: buy if last return is positive and sell if it's negative. 

Rolling window: buy if last N strategies is positive and sell if last N strategies is negative. 

Generally, this dynamic might be more pronounced intraday than interday. 

# Overall implementation pseudo-code 
- Get prices (daily/minute granularity)  
- Generate `log_returns` column with price shift method  
- Generate `position` column with `np.sign(data['returns'])`   
    - read: if today_price/ytd_price is positive, we buy; hence it's purely a function of returns. Imagine as, this will be the position we take at EOD for tomorrow.  
    - If you want to use more days, you do: `np.sign(data['returns'].rolling(3).mean())`  
- Generate strategy returns with `data['position'].shift(1) * data['returns']` 
    - read: Ytd's positions (we took at EOD) times  today's actual returns will give us the strategy returns  
- Generate overall returns `data[['returns', 'strategy']].dropna().cumsum().apply(np.exp).plot(figsize=(10, 6))`