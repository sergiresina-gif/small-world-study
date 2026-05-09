import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def plot_graph(G, title=""):
    nx.draw(G, with_labels=True, pos=nx.circular_layout(G))
    plt.title(title)
    plt.show()

def plot_lc_vs_beta(betas, L_norm, C_norm):
    plt.semilogx(betas, L_norm, label='L(β)/L(0)')
    plt.semilogx(betas, C_norm, label='C(β)/C(0)')
    plt.xlabel('β')
    plt.legend()
    plt.show()

def plot_3d_surface(results):
    """Plots a 3D surface of L as a function of N and K for each beta."""
    from mpl_toolkits.mplot3d import Axes3D

    for beta, data in results.items():
        N_unique = sorted(set(data['N_list']))
        K_unique = sorted(set(data['K_list']))
        L_grid = np.array(data['L_list']).reshape(len(K_unique), len(N_unique))
        N_grid, K_grid = np.meshgrid(N_unique, K_unique)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(N_grid, K_grid, L_grid, cmap='viridis', shade=True)
        ax.plot_surface(N_grid, K_grid, np.full_like(L_grid, 6),
                        color='red', alpha=0.5, edgecolor='red', linewidth=0.5)
        ax.set_zlim(0, 20)
        ax.set_xlabel('N')
        ax.set_ylabel('K')
        ax.set_zlabel('L(D)')
        plt.colorbar(surf, ax=ax, pad=0.1).set_label('L(D)')
        plt.title(f'beta = {beta}')
        plt.show()

def print_good_data(good_data):
    """Prints all (N, K, beta) combinations that achieved the target L."""
    print("\n===========")
    for N, K, beta, L_val in good_data:
        print(f"N={N}, K={K}, beta={beta}: L={L_val:.3f}")