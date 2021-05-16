import yfinance as yf

class Stock:

    def __init__(self) -> None:
        pass

    
    # download data from yahoo finance
    def download(self, stocks, interval, period):
        data = yf.download( \
            # tickers list or string as well
            # "SPY AAPL MSFT"
            tickers = stocks, \
            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo') 
            period = period, \
            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = interval, \
            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'ticker', \
            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust = True, \
            # download pre/post regular market hours data
            # (optional, default is False)
            prepost = True)
        return (data)


    # indicator SMA (simple moving average)
    def SMA(self, data, interval):
        return (data['Close'].rolling(window=interval).mean())


    # indicator EMA (exponential moving average)
    def EMA(self, data, interval):
        pass


    # indicator BB (bolllinger bands)
    def BBands(self, data, interval):
        pass


    # 1. Analyst
    # analyst the trend based on EMA
    def analyst(self, data):
        pass