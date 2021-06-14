from stockio.stock import Stock
from stockio.graph import Graph

if __name__ == '__main__':
    stock = Stock()

    # download data from yahoo
    df = stock.download("AALI.JK", "1d", "6mo")
    print(df)

    # show the graph
    graph = Graph()
    graph.render(df, "AALI Stock", "date", "close price")