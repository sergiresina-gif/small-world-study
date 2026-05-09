import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def anell_regular(N,K):
    """
    Generaters a regular ring graph

    Parameters:
        N:  Number of nodes
        K:  Degree of the graph
            Each node is connected to K//2 neighbours to the right 
            and K//2 to the left
    
    Returns:
        A: nx.Graph with N nodes and N*K//2 edges
    """
    A = nx.Graph()
    for node in range(N):
        for neighbour_right in range(1,K//2+1):
            # Connect with the neighbour at 'neighbour-right' distance to the right
            A.add_edge(node,( node+neighbour_right )%N )
            # Connect with the neighbour at 'neighbour-right' distance to the left (simetric process)
            # The %N ensures that the ring is circular
            A.add_edge(node,( node - neighbour_right )%N )
    return A

def erdos_renyi(N,K):
    """
    Generates a random graph following the Erdos-Renyi mode

    Parameters:
        N: Number of nodes
        K: Desired average degree
           The probability of existence of each edge is p = K/N
           On average each node has K neighbours

    Returns:
        B: random nx.Graph 
    """
    p = K/N # Chance of connection between a pair of nodes
    B = nx.Graph()
    for node in range(N):
        for node_2 in range(N):
            if node_2 != node: # Avoid auto-loops
                if np.random.random() < p: # Connection with a chance 'p'
                    B.add_edge(node,node_2)
    return B

def watts_strogatz(N,K, beta):
    """
    Generates a graph following the Watts-Strogatz model

    Starts with a regular ring graph and rewires each edge with a probability called 'beta':
    Deletes the original edge and reconnects it to a random node

    Parameters
    N: Number of nodes
    K: Initial degree inherited from the regular ring graph
    beta: Chance of rewiring [0,1]:
        0 -> Pure regular ring
        ~0.1 -> Small-world (high clustering, low distances)
        1 -> Almost random network

    Returns: 
        C: nx.Graph wirh small world topology
    """
    C = anell_regular(N,K) # Starting point: regular ring
    for node in range(N):
        for neighbour in list(C.neighbors(node)): # List won't be modified during the iteration
            if np.random.random() < beta:
                # Rewiring: remove the current edge
                C.remove_edge(node,neighbour)

                # Choose randomly a new neighbour different from the current one
                new_neighbour = np.random.randint(0,N)
                while (new_neighbour == node):
                    new_neighbour = np.random.randint(0,N)

                # Reconnects the node to the new random neighbour
                C.add_edge(node, new_neighbour)
    return C

def L(G):
    """
    Computes the average shortest path length of graph G using a built-in
    function from the module networkx
    """
    try:
        return nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        return float('inf')

def C(G):
    """
    Computes the average clustering coefficeint of graph G that corresponds to the
    ratio between the total number of edges between the neighbours and the maximum number
    of possible edges. We use a bult-in function from the module networkx
    """
    try:
        return nx.average_clustering(G)
    except nx.NetworkXError:
        return 0
    
def search_parameters(betas, N_range, K_range, target_L=6, tolerance=1):
    """
    Searches for (N, K, beta) combinations that produce a target average path length.

    Parameters:
        betas   : list of beta values to sweep
        N_range : range of N values e.g. range(100, 1000, 50)
        K_range : list of K values e.g. [4,5,6,7,8,9,10]
        target_L: target average path length (default 6)
        tolerance: accepted deviation from target_L (default 1)

    Returns:
        good_data: list of [N, K, beta, L_val] that satisfy |L - target| < tolerance
        results  : dict with keys=beta, values=dict with N_list, K_list, L_list
    """
    good_data = []
    results = {}

    for beta in betas:
        N_list, K_list, L_list = [], [], []
        for N in N_range:
            for K in K_range:
                D = watts_strogatz(N, K, beta)
                L_val = L(D)
                N_list.append(N)
                K_list.append(K)
                L_list.append(L_val)
                print(f"N={N}, K={K}, beta={beta}: L={L_val:.3f}")
                if abs(L_val - target_L) < tolerance:
                    good_data.append([N, K, beta, L_val])

        results[beta] = {'N_list': N_list, 'K_list': K_list, 'L_list': L_list}

    return good_data, results