import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import leaves_list, dendrogram

try:
    from fastcluster import linkage
except ImportError:
    from scipy.cluster.hierarchy import linkage


def get_cell_data(n=50, seed=0):
    np.random.seed(seed)
    cells_data = np.load('./data/cells_data.npy')

    sample_cells = np.random.choice(cells_data.shape[0], n, replace=False)

    D = pdist(cells_data[sample_cells, :], 'euclidean')
    Z = linkage(D, 'ward')

    return cells_data, Z, D

def get_random_data(n=50, seed=0):

    np.random.seed(seed)
    data = np.random.choice(10000, (n, 1), replace=False)
    D = pdist(data, 'euclidean')
    Z = linkage(D, 'ward')
    return data, Z, D


def run_polo(Z, D):
    from polo import optimal_leaf_ordering

    start_time = time.time()
    best_Z = optimal_leaf_ordering(Z, D)
    end_time = time.time()
    return end_time - start_time, best_Z


def run_orange3(Z, D):
    import Orange.clustering.hierarchical as orange_hier

    tree = orange_hier.tree_from_linkage(Z)
    start_time = time.time()
    orange_hier.optimal_leaf_ordering(tree, squareform(D))
    end_time = time.time()
    return end_time - start_time, None


def benchmark():
    random_data = []
    for n in range(4, 12):
        for i in range(3):
            data, z, d = get_random_data(2**n, i)
            polo_time, _ = run_polo(z, d)
            print(n, i, polo_time)
            random_data.append([n, i, polo_time])
    np.save('./data/random_data_benchmark.npy', np.array(random_data))

    cells_data = []
    for n in range(4, 13):
        for i in range(3):
            data, z, d = get_cell_data(2**n, i)
            polo_time, _ = run_polo(z, d)
            print(n, i, polo_time)
            cells_data.append([n, i, polo_time])
    np.save('./data/real_data_benchmark.npy', np.array(cells_data))
    
    orange_data = []
    for n in range(4, 12):
        for i in range(3):
            data, z, d = get_cell_data(2**n, i)
            oj_time, _ = run_orange3(z, d)
            print(n, i, oj_time)
            orange_data.append([n, i, oj_time])
    np.save('./data/real_data_orange3_benchmark.npy', np.array(orange_data))

def make_benchmark_figure():

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(1, 1, 1, xscale='linear', yscale='log')


    d1 = np.load('./data/random_data_benchmark.npy')
    d2 = np.load('./data/real_data_benchmark.npy')
    d3 = np.load('./data/real_data_orange3_benchmark.npy')

    ax.scatter(d1[:24, 0], d1[:24, 2], c='r', edgecolor='none', label='Random Data (Polo)')
    ax.scatter(d2[:24, 0], d2[:24, 2], c='green', edgecolor='none', label='Gene expression data (Polo)')
    ax.scatter(d3[:24, 0], d3[:24, 2], c='blue', edgecolor='none', label='Gene expression data (Orange3)')

    ax.legend(loc=2)
    ax.grid('on')
    ax.set_xlabel('log2(Number of leaves)')
    ax.set_ylabel('Run time, seconds')
    fig.tight_layout()
    fig.savefig('data/bench.png', dpi=75)

def make_figure():
    gs = gridspec.GridSpec(5, 1,
                       height_ratios=[3, 1, 2, 3, 1],
                       hspace=0)

    data, Z, D = get_random_data(100, 0)
    order = leaves_list(Z)


    runtime, opt_Z = run_polo(Z, D)
    opt_order = leaves_list(opt_Z)

    fig = plt.figure(figsize=(5,5))
    axd1 = fig.add_subplot(gs[0,0])
    axd1.set_title("Random numbers, clustered using Ward's criterion, default linear ordering.", fontsize=9)
    dendrogram(Z, ax=axd1, link_color_func=lambda k: 'k')
    axd1.set_xticklabels(data[order].reshape(-1))
    axd1.set_xticks([])
    axd1.set_yticks([])

    axh1 = fig.add_subplot(gs[1,0])
    axh1.matshow(data[order].reshape((1,-1)), aspect='auto', cmap='RdBu', vmin=0, vmax=10000)
    axh1.set_xticks([])
    axh1.set_yticks([])

    axd2 = fig.add_subplot(gs[3,0])
    axd2.set_title("The same hierarchical clustering, arranged for optimal linear ordering.", fontsize=9)
    dendrogram(opt_Z, ax=axd2, link_color_func=lambda k: 'k')
    axd2.set_xticklabels(data[opt_order].reshape(-1))
    axd2.set_xticks([])
    axd2.set_yticks([])

    axh2 = fig.add_subplot(gs[4,0])
    axh2.matshow(data[opt_order].reshape((1,-1)), aspect='auto', cmap='RdBu', vmin=0, vmax=10000)
    axh2.set_xticks([])
    axh2.set_yticks([])

    fig.savefig('data/demo.png', dpi=130)


if __name__=="__main__":
    make_figure()
    # benchmark()
    #make_benchmark_figure()
