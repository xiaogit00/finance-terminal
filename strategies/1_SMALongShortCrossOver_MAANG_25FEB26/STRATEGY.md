# General idea of strategy
We construct 2 SMAs, one short SMA of around 40 day, and another long SMA of around 200 days. 

The idea is that when the short SMA moves above the long SMA, it indicates that there is an upward trend, and so we buy. 

When the short SMA drops and cuts through the long SMA, we sell. 

# Overall implementation pseudo-code 
After creating two columns, SMA1 and SMA2, you'll mark the periods where SMA1 > SMA2 as 1, and SMA < SMA2 as -1. Using the daily charts, we take a long position when it's 1, and a short position when it's -1. To get cumulative returns, we simply sum up the log returns over a period. 

