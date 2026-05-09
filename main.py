from netfunctions import *
from config import N, K, betas, do_plot
from plots import plot_graph, plot_lc_vs_beta, plot_3d_surface, print_good_data

# Initialization of the different networks
A = anell_regular(N, K)
B = erdos_renyi(N, K)
D = watts_strogatz(N, K, beta=0.1)

print(f"{'Xarxa':<20} {'L':>8} {'C':>8}")
print(f"{'Anell regular':<20} {L(A):>8.4f} {C(A):>8.4f}")
print(f"{'Erdos-Renyi':<20} {L(B):>8.4f} {C(B):>8.4f}")
print(f"{'Watts-Strogatz':<20} {L(D):>8.4f} {C(D):>8.4f}")

if do_plot:
    plot_graph(A, "Anell regular")
    plot_graph(B, "Erdos-Renyi")
    plot_graph(D, "Watts-Strogatz")

# Comparasion: Normalized values of L vs normalized values of C0
C0 = C(A)
L0 = L(A)
L_norm, C_norm = [], []

for beta in betas:
    W = watts_strogatz(N, K, beta)
    L_norm.append(L(W) / L0)
    C_norm.append(C(W) / C0)

if do_plot:
    plot_lc_vs_beta(betas, L_norm, C_norm)


betas      = [0.01, 0.05, 0.1]
N_range    = range(100, 1000, 50)
K_range    = [4, 5, 6, 7, 8, 9, 10]

good_data, results = search_parameters(betas, N_range, K_range)

if do_plot:
    plot_3d_surface(results)

print_good_data(good_data)






