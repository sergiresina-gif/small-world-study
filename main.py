import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Input of N (number of inhabitants) and k (neighbours)
# print( "Input number of nodes (N): ")
# N = int(input())
# print( "Input number of neighbours (k): ")
# k = int(input())

N = 100
K = 20

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


# for beta in [0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]:
#     D = watts_strogatz(N,K, beta)

#     print("Waltz-Strogatz")
#     print(beta)
#     print("L = ", L(D))
#     print("C = ", C(D))
#     print()

#     if ( do_you_want_plots ):
#         nx.draw(D, with_labels=True, pos=nx.circular_layout(D, scale=100))
#         plt.show()

from mpl_toolkits.mplot3d import Axes3D


good_data = []
for beta in [0.01, 0.05, 0.1]:
    N_list = []
    K_list = []
    L_list = []

    for N in range(100,1000,50):
        for K in [4,5,6,7,8,9,10]:
            D = watts_strogatz(N,K, beta)
            L_val = L(D)
            N_list.append(N)
            K_list.append(K)
            L_list.append(L_val)
            print(f"Amb N={N}, K={K} i beta={beta}: tenim {L_val}")
            if ( abs(L_val -6) < 1 ):
                good_data.append([N,K,beta,L_val])
        

    N_unique = sorted(set(N_list))
    K_unique = sorted(set(K_list))
    L_grid = np.array(L_list).reshape(len(K_unique), len(N_unique))
    N_grid, K_grid = np.meshgrid(N_unique, K_unique)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(N_grid, K_grid, L_grid, cmap='viridis', shade=True)

    ax.set_zlim(0, 20)

    indicator_surface = ax.plot_surface(N_grid, K_grid, 
                                     np.full_like(L_grid, 6), 
                                     color='red', 
                                     alpha=0.5,
                                     edgecolor='red',
                                     linewidth=0.5)

    cbar = plt.colorbar(surf, ax=ax, pad=0.1)
    cbar.set_label('L(D)', fontsize=12)

    ax.set_xlabel('N')
    ax.set_ylabel('K')
    ax.set_zlabel('L(D)')
    plt.show()

print("\n\n===========")
for element in good_data:
    print(f"Amb N={element[0]}, K={element[1]} i beta={element[2]}: tenim {element[3]}")

