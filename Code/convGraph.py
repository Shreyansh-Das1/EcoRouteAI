import networkx as nx
import numpy as np
import rasterio
import pickle

with rasterio.open(r"Dataset\CostSurface.tif") as src:
    costSurface = src.read(1)
    profile = src.profile

row,col = costSurface.shape

graph = nx.grid_2d_graph(row,col)

for u , v in graph.edges():
    costU = costSurface[u[0], u[1]] # 0th index is row and 1st index is column
    costV = costSurface[v[0], v[0]]
    if costU == 9999 or costV ==9999:
        graph[u][v]['weight'] = float('inf')
    else:
        graph[u][v]['weight'] = (costU + costV) / 2.0

graph.graph['crs'] = profile['crs'].to_wkt()
graph.graph['transform'] = list(profile['transform'])

with open("costGraph.gpickle", "wb") as dst:
    pickle.dump(graph, dst, protocol = pickle.HIGHEST_PROTOCOL) #Uses latest and most efficient format