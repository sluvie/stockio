import yfinance as yf
import numpy as np
import pandas as pd
import stockio.indicator as ind

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


    # get ema prediction (buy, sell, netral)
    def EMA(self, data, ema1 = 9, ema2 = 21, ema3 = 55, ema4 = 100, ema5 = 200):
        # get ema data
        df_ema1 = ind.iMA(data, ema1, 0, 'EMA')
        df_ema2 = ind.iMA(data, ema2, 0, 'EMA')
        df_ema3 = ind.iMA(data, ema3, 0, 'EMA')
        df_ema4 = ind.iMA(data, ema4, 0, 'EMA')
        df_ema5 = ind.iMA(data, ema5, 0, 'EMA')

        data['ema1'] = df_ema1
        data['ema2'] = df_ema2
        data['ema3'] = df_ema3
        data['ema4'] = df_ema4
        data['ema5'] = df_ema5

        return (data)


    # get macd prediction (buy, sell, netral)
    def MACD(self, data, fast_period = 12, slow_period = 26, signal_period = 9):
        df_macd = ind.iMACD(data, fast_period, slow_period, signal_period)
        
        df_ema1 = ind.iMA(data, fast_period, 0, 'EMA')
        df_ema2 = ind.iMA(data, slow_period, 0, 'EMA')
        
        # get trend up based on ema, 1 = up, 0 = netral
        data['trend_up'] = np.where((df_ema1 > df_ema2), 1, 0)
        
        # get trend down based on ema, 1 = down, 0 = netral
        data['trend_down'] = np.where((df_ema1 < df_ema2), 1, 0)
        
        data['main'] = df_macd['Main']
        data['signal'] = df_macd['Signal']

        return (data)

    
    # get data bollinger (buy, sell, netral)
    def buy_sell_bollinger(self, data):
        UpperBollinger = data['Upper']
        BaseBollinger = data['Median']
        LowerBollinger = data['Lower']
        AppliedPrice = data['Close']

        BuyEntry = (UpperBollinger < AppliedPrice)
        SellEntry = (LowerBollinger > AppliedPrice)
        BuyExit = ((BaseBollinger > AppliedPrice))
        SellExit = ((BaseBollinger < AppliedPrice))

        return (BuyEntry, SellEntry, BuyExit, SellExit)

    def bollinger(self, data):
        Bollinger = ind.iBands(data, 20, 2)
        chart = pd.DataFrame(
            { 'Close': data['Close'], 'Median': Bollinger['Base'], 'Upper': Bollinger['Upper'], 'Lower': Bollinger['Lower'] }
        )

        # Store the buy and sell data into a variable
        position = self.buy_sell_bollinger(chart)
        storage = pd.DataFrame({
            'Close': data['Close'],
            'Upper': chart['Upper'],
            'Median': chart['Median'],
            'Lower': chart['Lower'],
            'buy_signal': position[0],
            'sell_signal': position[1],
            'buy_exit': position[2],
            'sell_exit': position[3],
        })

        data['upper'] = storage['Upper']
        data['median'] = storage['Median']
        data['lower'] = storage['Lower']

        # get trend up based on buy signal
        data['trend_up'] = np.where((storage['Close'] < storage['Upper']) & (storage['Close'] > storage['Median']), 1, 0)
        
        # get trend down based on sell signal
        data['trend_down'] = np.where((storage['Close'] < storage['Median']) & (storage['Close'] > storage['Lower']), 1, 0)

        return (data)


    # get data stochastic (buy, sell, netral)
    def stochastic(self, data):
        df = ind.iStochastic(data, 14, 3, 3, "EMA")

        data['signal'] = df['Signal']
        data['main'] = df['Main']
        data['overbought'] = np.where((df['Main'] >= 80), 1, 0)
        data['oversell'] = np.where((df['Main'] <= 20), 1, 0)

        return (data)