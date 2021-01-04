import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import ete3
from ete3 import Tree
import math
import numpy

def find_root(G,node):
    temp=list(G.predecessors(node))
    if len(temp)>0: #True if there is a predecessor, False otherwise
        root = find_root(G,list(temp)[0])
    else:
        root = node
    return root

def analyzetree(component, directedG, outputf):
    G = directedG.subgraph(component.nodes)
    for node in G.nodes:
        root = find_root(G, node)
    
    temp = nx.shortest_path_length(G,root)
    treeheight = str(max(temp.values()))
    subtrees = {node:ete3.Tree(name=node) for node in G.nodes()}
    [*map(lambda edge:subtrees[edge[0]].add_child(subtrees[edge[1]]), G.edges())]
    tree = subtrees[root]
    return treeheight, root
    

def plotgraph(component, directedG):
    G = directedG.subgraph(component.nodes)
    seed = 13648  # Seed random number generators for reproducibility
    pos = nx.spring_layout(G, seed=seed)
    M = G.number_of_edges()
    
    cmap = plt.cm.plasma

    nodes = nx.draw_networkx_nodes(G, pos, node_size=100, node_color="orange")
    edges = nx.draw_networkx_edges(
    G,
    pos,
    node_size=100,
    arrowstyle="->",
    arrowsize=20,
    edge_color="green",
    width=2)

    label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
    labels = nx.draw_networkx_labels(G, pos, font_size=14, bbox=label_options)

    ax = plt.gca()
    ax.set_axis_off()
    plt.show()

def activate_nodes(g, node):               
    for pred in g.predecessors(node):
        activate_nodes(g, pred)


def fivepointSummary(inputFile):
    x = pd.read_csv(inputFile, header=None)
    temp = x.iloc[:,0]
    print(numpy.min(temp))
    print(numpy.max(temp))
    print(numpy.std(temp))
    print(numpy.mean(temp))
    print(numpy.median(temp))


def getTreeStatistics(forkedgesFile, forkTreeSize, forkTreeHeight, forkFromSourceorNot):
    rootfolder = "C:/Users/sophi/PycharmProjects/kaggle/MSR21/"
    df = pd.read_csv(rootfolder+forkedgesFile)
    df.head()
    G = nx.from_pandas_edgelist(df, 'parentKernelId', 'childKernelId')
    print(nx.info(G))

    print("total number of fork trees:"+str(nx.number_connected_components(G)))
    A=list(G.subgraph(c) for c in nx.connected_components(G))
    directedG = nx.from_pandas_edgelist(df, source='parentKernelId',target='childKernelId', edge_attr=None, create_using=nx.DiGraph())

    counter=0
    sourceKernels = {}
    with open(rootfolder+forkTreeSize, 'w') as outputf, open(rootfolder+forkTreeHeight, 'w') as heightf:
        for component in A:
            counter+=1
            outputf.write(str(len(set(component)))+'\n')
            height, sourcekernelId = analyzetree(component, directedG,outputf)
            sourceKernels[sourcekernelId]= True
            heightf.write(height+'\n')
    
    with open(rootfolder+forkFromSourceorNot, 'w') as outputf:
        for index, row in df.iterrows():
            child, parent = row['childKernelId'], row['parentKernelId']
            forkedfromSource =  parent in sourceKernels.keys()
            outputf.write(str(child)+','+str(parent)+','+ str(forkedfromSource)+'\n')


if __name__ == '__main__':
    rootfolder = "C:/Users/sophi/PycharmProjects/kaggle/MSR21/"
    forkedgesFile = "data/forkedges_selfexclude.csv"
    forkTreeSize= "data/forktreesize_selfex.csv"
    forkTreeHeight= "data/heights_selfex.csv"
    forkFromSourceorNot= "data/forkFromSourceorNot_selfex.csv"
    getTreeStatistics(forkedgesFile, forkTreeSize, forkTreeHeight, forkFromSourceorNot)

    fivepointSummary(rootfolder+forkTreeSize)
    fivepointSummary(rootfolder+forkTreeHeight)

     
    
