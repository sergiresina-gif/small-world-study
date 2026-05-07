import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Input of N (number of inhabitants) and k (neighbours)
# print( "Input number of nodes (N): ")
# N = int(input())
# print( "Input number of neighbours (k): ")
# k = int(input())

N = 500
K = 4

do_you_want_plots = False

# print("Input what network generating algorythm you want:")
# print( "1. Xarxa en anell regular \n2. Erdös-Rényi \n3. Watts-Strogatz")
# choice = int(input())

# A = nx.Graph()
# for node in range(N):
#     A.add_node(f"{node}")

# Cas a
def anell_regular(N,K):
    A = nx.Graph()
    for node in range(N):
        for neighbour_right in range(1,K//2+1):
            A.add_edge(node,( node+neighbour_right )%N )
            A.add_edge(node,( node - neighbour_right )%N )
    return A


def erdos_renyi(N,K):
    p = K/N
    B = nx.Graph()
    for node in range(N):
        for node_2 in range(N):
            if node_2 != node:
                if np.random.random() < p:
                    B.add_edge(node,node_2)
    return B

def watts_strogatz(N,K, beta):
    C = anell_regular(N,K)
    for node in range(N):
        for neighbour in list(C.neighbors(node)):
            if np.random.random() < beta:
                C.remove_edge(node,neighbour)
                new_neighbour = np.random.randint(0,N)
                while (new_neighbour == node):
                    new_neighbour = np.random.randint(0,N)
                C.add_edge(node, new_neighbour)
    return C
                    


def L(G):
    try:
        return nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        return float('inf')

def C(G):
    try:
        return nx.average_clustering(G)
    except nx.NetworkXError:
        return 0

# match choice:
#     case 1:
#         A = anell_regular(N,k)
#     case 2:
#         pass    

A = anell_regular(N,K)

print("Anell regular:")
print("L = ", L(A))
print("C = ", C(A))
print()

if ( do_you_want_plots ):
    nx.draw(A, with_labels=True, pos=nx.circular_layout(A, scale=100))
    plt.show()

B = erdos_renyi(N,K)

print("Erdo-Algo:")
print("L = ", L(B))
print("C = ", C(B))
print()

if ( do_you_want_plots ):
    nx.draw(B, with_labels=True, pos=nx.circular_layout(B, scale=100))
    plt.show()

D = watts_strogatz(N,K, 0.1)

print("Waltz-Strogatz")
print("L = ", L(D))
print("C = ", C(D))
print()

if ( do_you_want_plots ):
    nx.draw(D, with_labels=True, pos=nx.circular_layout(D, scale=100))
    plt.show()