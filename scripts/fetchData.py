import yfinance as yf
import sys 
ticker = sys.argv[1]
from pathlib import Path

def fetchPrice(ticker):
    '''
    Fetches the full price data from yFinance and saves it as CSV in data/price 
    
    :param ticker: Symbol to fetch
    '''
    # print(Path(__file__).resolve().parent.parent)
    data = yf.download(ticker, period='max')
    print("Successfully downloaded data from yFinance")
    data.to_csv(f'data/price/{ticker}_full.csv')
    print(f"Successfully saved to /data/price/{ticker}_full.csv")

fetchPrice(ticker)