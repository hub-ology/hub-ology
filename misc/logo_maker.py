"""
Inspired by: http://networkx.lanl.gov/examples/drawing/knuth_miles.html

This utility will generate the hub-ology logo based on 
2010 census data for towns in Spartanburg, South Carolina.
PNG and SVG graph outputs are generated.

Since the goal of hub-ology is to inspire rural areas to do 'big tech'
it's only fitting that the logo generation for the site 
provide some educational value.  The utility uses 2010 census data 
to get population information for towns in Spartanburg, SC.
It uses the geopy module to determine the latitude and longitude 
for each town.  It uses networkx and matplotlib to generate 
an undirected graph of the towns connecting to Spartanburg
(the hub-city).  The distances between nodes represent miles 
between the towns and Spartanburg.  The size of each node 
is based on the 2010 population for the town it represents.

"""

from geopy import distance
from matplotlib import pyplot
from matplotlib.colors import ColorConverter
from matplotlib.colors import ListedColormap
import networkx
import csv
import sys

def load_census_data(census_file):
    with open(census_file, "rb") as csvfile:
        reader = csv.reader(csvfile)
        for rownum, row in enumerate(reader):
            if rownum == 0:
                headers = row
            else:
                town = {}
                for index, field in enumerate(row):
                    town[headers[index]] = field
                yield town

def clean_town_data(raw_towns):
    towns = []
    for raw_town in raw_towns:
        town = {}
        town['name'] = raw_town['GEO'].replace(' CDP,', ',').replace(' town,',',').replace(' city,',',')
        town['population'] = int(raw_town['Population Count (100%)'][1:])
        town['latlng'] = (float(raw_town['Internal Point (Latitude)'][1:]) , float(raw_town['Internal Point (Longitude)'][1:]))
        towns.append(town)
    return towns

def calculate_distances(towns, hub_town=None):
    for start_town in towns:
        dist_info = {}
        for end_town in towns:
            if start_town['name'] != end_town['name']:
                record_distance = True
                if hub_town is not None:
                    if end_town['name'] != hub_town['name']:
                        record_distance = False
                if record_distance:    
                    dist_info[end_town['name']] = distance.distance(start_town['latlng'], end_town['latlng']).miles
        start_town['distances'] = dist_info

def main(census_file):
    #exclude some towns to get output that's less cluttered.
    #no offense to any of these towns...it's not personal -- just avoiding a lot of overlap
    exclusions = ('Greer, South Carolina', 'Roebuck, South Carolina', 
                  'Central Pacolet, South Carolina', 'Southern Shops, South Carolina', 
                  'Lyman, South Carolina', 'Inman Mills, South Carolina', 
                  'Boiling Springs, South Carolina', 'Valley Falls, South Carolina', 
                  'Fairforest, South Carolina', 'Arcadia, South Carolina', 
                  'Wellford, South Carolina', 'Saxon, South Carolina')
    
    towns = clean_town_data(load_census_data(census_file))
    calculate_distances(towns, towns[-5])
    #calculate_distances(towns)
        
    miles_graph = networkx.Graph()
    miles_graph.position = {}
    miles_graph.population = {}
    
    for town in towns:
        #print town
        if town['name'] not in exclusions:            
            miles_graph.add_node(town['name'])
            miles_graph.position[town['name']] = (town['latlng'][1], town['latlng'][0])
            miles_graph.population[town['name']] = town['population']
            for end_town, miles in town['distances'].items():
                miles_graph.add_edge(town['name'], end_town, weight=int(miles))
        
    old_glory = ListedColormap([ColorConverter().to_rgb('#FFFFFF'), 
                                ColorConverter().to_rgb('#0052A5'),
                                ColorConverter().to_rgb('#E0162B')], name='Old Glory')        

    orange_hex = '#FF6600'
    blaze_orange = ListedColormap([ColorConverter().to_rgb(orange_hex)], name='Blaze Orange')

    #Old Glory Logo
    pyplot.figure(figsize=(12,12))
    networkx.draw(miles_graph,miles_graph.position,
                node_size=[miles_graph.population[v] for v in miles_graph],
                node_color=range(len(miles_graph)),
                cmap=old_glory,
                with_labels=False, width=2)

    #Save the graph in png and svg formats
    pyplot.savefig("logo.png", dpi=300, transparent=True)    
    pyplot.savefig("logo.svg", transparent=True)       


    #Blaze Orange Logo
    pyplot.figure(figsize=(12,12))
    networkx.draw(miles_graph,miles_graph.position,
                node_size=[miles_graph.population[v] for v in miles_graph],
                node_color=range(len(miles_graph)),
                cmap=blaze_orange, 
                with_labels=False, width=2, edge_color=orange_hex)

    #Save the graph in png and svg formats
    pyplot.savefig("orange_logo.png", dpi=300, transparent=True)    
    pyplot.savefig("orange_logo.svg", transparent=True)       

if __name__ == "__main__":
    if len(sys.argv) > 1:
        census_file = sys.argv[1]
    else:
        census_file = 'data/Spartanburg_2010_Census/DEC_10_PL_G001_ann.csv'
    
    main(census_file)