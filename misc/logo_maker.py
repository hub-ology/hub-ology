"""
Inspired by: http://networkx.lanl.gov/examples/drawing/knuth_miles.html
"""

from geopy import distance, geocoders
from matplotlib import pyplot
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
        towns.append(town)
    return towns

def geotag_towns(towns):
    g = geocoders.Google()

    for town in towns:
        geoinfo = g.geocode(town['name'])
        town['latlng'] = geoinfo[1]

def calculate_distances(towns, hubtown=None):    
    for start_town in towns:
        dist_info = {}
        for end_town in towns:
            if start_town['name'] != end_town['name']:
                record_distance = True
                if hubtown is not None:
                    if end_town['name'] != hubtown['name']:
                        record_distance = False
                if record_distance:    
                    dist_info[end_town['name']] = distance.distance(start_town['latlng'], end_town['latlng']).miles
        start_town['distances'] = dist_info

def main(census_file):
    towns = clean_town_data(load_census_data(census_file))
    geotag_towns(towns)
    calculate_distances(towns, towns[-5])
    #calculate_distances(towns)
        
    miles_graph = networkx.Graph()
    miles_graph.position = {}
    miles_graph.population = {}
    
    for town in towns:
        print town
        miles_graph.add_node(town['name'])
        miles_graph.position[town['name']] = (town['latlng'][1], town['latlng'][0])
        miles_graph.population[town['name']] = town['population']
        for end_town, miles in town['distances'].items():
            miles_graph.add_edge(town['name'], end_town, weight=int(miles))
    
    graph = networkx.Graph()
    for node in miles_graph:
        graph.add_node(node)
    
    for (u,v,d) in miles_graph.edges(data=True):
        #if d['weight'] < 20:
        graph.add_edge(u,v)
    
    pyplot.figure(figsize=(12,12))
    # with nodes colored by degree sized by population
    node_color=[float(graph.degree(v)) for v in graph]
    networkx.draw(graph,miles_graph.position,
                node_size=[miles_graph.population[v] for v in graph],
                node_color=node_color,
                with_labels=False)

    # scale the axes equally
    #pyplot.xlim(-5000,500)
    #pyplot.ylim(-2000,3500)

    pyplot.savefig("logo.png")    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        census_file = sys.argv[1]
    else:
        census_file = 'data/Spartanburg_2010_Census/DEC_10_PL_G001_ann.csv'
    
    main(census_file)