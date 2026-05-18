import networkx as nx
import matplotlib.pyplot as plt
# funció per dibuixar les xarxes
def draw_graph(G: nx.Graph, title: str, pos=None):
    if pos is None:
        pos = nx.circular_layout(G, scale=100)
    nx.draw(G, with_labels=True, pos=pos)
    plt.title(title)
    plt.show()

def draw_graphs(graphs: dict[str, nx.Graph]):
    n = len(graphs)
    pos = nx.spring_layout(list(graphs.values())[0], seed=123)

    fig, axes = plt.subplots(1, n, figsize=(5*n, 5))
    for ax, (title, G) in zip(axes, graphs.items()):
        pos = nx.circular_layout(G, scale=100)
        nx.draw(G, with_labels=True, pos=pos, ax=ax)
        ax.set_title(title)
    plt.show()