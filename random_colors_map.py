import matplotlib.pyplot as plt 
import osmnx as ox
import networkx as nx
import pandas as pd 
import random
import numpy as np

place = 'Δήμος Θεσσαλονίκης'
graph = ox.graph_from_place(place)
fig, ax = ox.plot_graph(graph)


nodes, edges = ox.graph_to_gdfs(graph)
area = ox.geocode_to_gdf(place)

buildings = ox.geometries_from_place(place, tags={'building':True})

#Create a random number for each building in thee map
buildings['color'] = [ random.randint(1,15)  for k in buildings.index]
print(buildings['color'])

##Now match each of these numbers to a dictionary of colors for matplotlib
colors = {1:"palegoldenrod", 2:"mediumaquamarine",
            3:"peru", 4:"mistyrose", 5:"plum",
            6:"pink", 7:"indianred", 8:"burlywood",
            9:"rosybrown", 10:"olivedrab", 11:"darksalmon",
            12:"forestgreen", 13:"slateblue", 14:"indigo",
            15:"firebrick"}


for i,j in buildings['color'].iteritems():
    #lis.append(colors[j])
    buildings['color'][i] = colors[j]

#print(lis)

def plot():
    #Plot the data from OSM
    fig, ax = plt.subplots(figsize=(12,8))

    # Plot the footprint
    area.plot(ax=ax, facecolor='black', edgecolor ='dimgrey')

    # Plot street edges
    edges.plot(ax=ax, linewidth=0.5, edgecolor='black')

    # Plot parkings
    buildings.plot(ax=ax, color=buildings['color'], edgecolor ='dimgrey', alpha=0.7, markersize=10, marker = 's', zorder = 10)

    plt.title('Buildings in \n Central Thessaloniki, Greece', fontsize=20)


    plt.show()
plot()
