from stockio.stock import Stock

if __name__ == '__main__':
    stock = Stock()
    df = stock.download("AAPL", "1d", "6mo")
    print(df)