from stockio.stock import Stock
from stockio.graph import Graph

if __name__ == '__main__':
    stock = Stock()
    df = stock.download("AAPL", "1d", "6mo")
    print(df)

    graph = Graph()
    graph.render(df, "AAPL Stock", "date", "close price")