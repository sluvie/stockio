import matplotlib.pyplot as plt

class Graph:

    def __init__(self) -> None:
        pass

    def render(self, data, \
            title, xlabel = "", ylabel = ""):

        plt.figure(figsize=(10,10))
        plt.plot(data.index, data['Close'])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()