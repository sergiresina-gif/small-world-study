import networkx as nx
import matplotlib.pyplot as plt

# Input of N (number of inhabitants) and k (neighbours)
# print( "Input number of nodes (N): ")
# N = int(input())
# print( "Input number of neighbours (k): ")
# k = int(input())

N = 10
k = 4

# print("Input what network generating algorythm you want:")
# print( "1. Xarxa en anell regular \n2. Erdös-Rényi \n3. Watts-Strogatz")
# choice = int(input())

# A = nx.Graph()
# for node in range(N):
#     A.add_node(f"{node}")

# Cas a
def anell_regular(N,k):
    A = nx.Graph()
    for node in range(N):
        for neighbour_right in range(1,k//2+1):
            A.add_edge(node,( node+neighbour_right )%N )
            A.add_edge(node,( node - neighbour_right )%N )
    return A

def L(G):
    return nx.average_shortest_path_length(G)

def C(G):
    return nx.average_clustering(G)

# match choice:
#     case 1:
#         A = anell_regular(N,k)
#     case 2:
#         pass    

A = anell_regular(N,k)

print("L = ", L(A))
print("C = ", C(A))

nx.draw_spring(A, with_labels=True)
plt.show()


