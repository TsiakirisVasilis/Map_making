import geopandas as gpd
import matplotlib.pyplot as plt 
import osmnx as ox
import networkx as nx
import pandas as pd 
import fiona.crs

#Plot the place
place = 'Δήμος Θεσσαλονίκης'
graph = ox.graph_from_place(place)
fig, ax = ox.plot_graph(graph)

#Convert the place to a geodataframe, geocode it
nodes, edges = ox.graph_to_gdfs(graph)
area = ox.geocode_to_gdf(place)
print(type(area))

#Get data geometries
parking = ox.geometries.geometries_from_place(place,  tags = {"parking":True, "parking_space":True}) 
historic = ox.geometries.geometries_from_place(place, tags = {"historic":True})
green = ox.geometries.geometries_from_place(place, tags = {"leisure":True})
bars = gpd.read_file('C:\\Users\\Bill Tsiakiris\\Python\\export.geojson')
restaurant = gpd.read_file(' C:\\Users\\Bill Tsiakiris\\Python\\export (1).geojson')
pubs = gpd.read_file('C:\\Users\\Bill Tsiakiris\\Python\\export (2).geojson')
cafes = gpd.read_file('C:\\Users\\Bill Tsiakiris\\Python\\export (3).geojson')



def plot():
    #Plot the data from OSM
    fig, ax = plt.subplots(figsize=(12,8))

    # Plot the footprint
    area.plot(ax=ax, facecolor='whitesmoke', edgecolor ='dimgrey')

    # Plot street edges
    edges.plot(ax=ax, linewidth=0.1, edgecolor='dimgrey')

    # Plot parkings
    parking.plot(ax=ax, color='red', alpha=0.7, markersize=10, marker = 's', zorder = 10)
    historic.plot(ax=ax, color='gold', alpha=0.7, markersize=10, marker = 's', zorder = 10)
    green.plot(ax=ax, color='green', alpha=0.7, markersize=10, marker = 's', zorder = 10)
    bars.plot(ax=ax, color='violet', alpha=0.7, markersize=10, marker = 's', zorder = 10)
    restaurant.plot(ax=ax, color='violet', alpha=0.7, markersize=10, marker = 's', zorder = 10)
    pubs.plot(ax=ax, color='violet', alpha=0.7, markersize=10, marker = 's', zorder = 10)
    cafes.plot(ax=ax, color='violet', alpha=0.7, markersize=10, marker = 's', zorder = 10)


    ax.scatter(22.9, 40.65, color = 'red', marker = 's',label = 'Parking Areas')
    ax.scatter(22.9, 40.65, color = 'gold', marker = 's', s = 12, label = 'Historc points of interest')
    ax.scatter(22.9, 40.65, color = 'green', marker = 's', s = 12, label = 'Urban green')
    ax.scatter(22.9, 40.65, color = 'violet', marker = 's', s = 12, label = 'Restaurants, bars, pubs, coffe houses')


    plt.title('Amenities in Thessaloniki, Greece', fontsize = 20)
    plt.legend()
    plt.tight_layout()
    plt.show()


plot()