from stockio.stock import Stock
from stockio.graph import Graph

if __name__ == '__main__':
    emiten = "GBPJPY=X"
    #emiten = "GC=F"
    #emiten = "BRIS.JK"

    stock = Stock()

    # download data from yahoo
    df = stock.download(emiten, "5m", "1mo")
    
    # predict ema data
    df_ema = df.copy()
    df_ema = stock.EMA(df_ema, 5, 10, 20, 50, 100)
    print(df_ema)

    # predict macd data
    df_macd = df.copy()
    df_macd = stock.MACD(df_macd)
    print(df_macd)

    # predict bollinger data
    df_bollinger = df.copy()
    df_bollinger = stock.bollinger(df_bollinger)
    print(df_bollinger)

    # predict stochastic data
    df_stochastic = df.copy()
    df_stochastic = stock.stochastic(df_stochastic)
    print(df_stochastic)

    # ambil data tail (main data)
    data = df.tail(2).head(1)
    close_value = data['Close'][0]

    # ema data
    data_ema = df_ema.tail(1)
    ema_5 = data_ema['ema1'][0]
    ema_10 = data_ema['ema2'][0]
    ema_20 = data_ema['ema3'][0]
    ema_50 = data_ema['ema4'][0]
    ema_100 = data_ema['ema5'][0]
    # trend ema
    trend_ema1 = 1 if ema_5 > ema_10 else 0
    trend_ema2 = 1 if ema_10 > ema_20 else 0
    trend_ema3 = 1 if ema_20 > ema_50 else 0
    trend_ema4 = 1 if ema_50 > ema_100 else 0

    # macd data
    data_macd = df_macd.tail(2).head(1)
    trend_macd = 1 if data_macd['trend_up'][0] == 1 else (-1 if data_macd['trend_down'][0] == 1 else 0)
    
    # bollinger data
    data_bollinger = df_bollinger.tail(2).head(1)
    trend_bollinger = 1 if data_bollinger['trend_up'][0] == 1 else (-1 if data_bollinger['trend_down'][0] else 0)
    
    # stochastic data
    data_stochastic = df_stochastic.tail(2).head(1)
    trend_stochastic = 1 if data_stochastic['overbought'][0] == 1 else (-1 if data_stochastic['oversell'][0] == 1 else 0)
    main_stochastic = data_stochastic['main'][0]

    # percentage decission
    # ema   : 5 5 10 10
    # macd  : 20
    # boll  : 20
    # sto   : 30
    percentage_buy = 0
    percentage_sell = 0
    percentage_buy = \
        (5 if ema_5 > ema_10 else 0) + (5 if ema_10 > ema_20 else 0) + (10 if ema_20 > ema_50 else 0) + (10 if ema_50 > ema_100 else 0) + \
        (30 if data_macd['trend_up'][0] == 1 else 0) + \
        (10 if data_bollinger['trend_up'][0] == 1 else 0) + \
        ((main_stochastic - 80 if main_stochastic > 80 else 0) / 20) * 30
    percentage_sell = \
        (0 if ema_5 > ema_10 else 5) + (0 if ema_10 > ema_20 else 5) + (0 if ema_20 > ema_50 else 10) + (0 if ema_50 > ema_100 else 10) + \
        (30 if data_macd['trend_down'][0] == 1 else 0) + \
        (10 if data_bollinger['trend_down'][0] == 1 else 0) + \
        ((main_stochastic if main_stochastic < 20 else 0) / 20) * 30
    trend = 1 if (percentage_buy > percentage_sell) else -1

    # find best price for hit
    sum_all = 0
    df_avg = df.tail(1*24)
    for x in range(0, len(df_avg)):
        sum_all = sum_all + df_avg['Close'][x]
    avg_all = sum_all / (len(df_avg))


    # TP / SL
    # EURUSD = 0.0020
    # GBPUSD = 0.0015
    # EURJPY = 0.15
    # XAUUSD = 5
    tp = avg_all + 0.15
    sl = avg_all - 0.15

    print("")
    print("Emiten           : {}".format(emiten))
    print("Percentage buy   : {}".format(percentage_buy))
    print("Percentage sell  : {}".format(percentage_sell))
    print("Trend            : {}".format("buy" if (trend == 1) else ("sell" if (trend == -1) else "netral")))
    print("")
    print("Price            : {}".format(close_value))
    print("Condition        : {}".format(avg_all))
    print("Take Profit      : {}".format(tp if (trend == 1) else sl))
    print("Stop Loss        : {}".format(sl if (trend == 1) else tp))
    print("")



