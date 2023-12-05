import random
import pdb
import class_import as ci
from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import sys
import kaleido
import json


random.seed(0)

#set g with global variables
g = ci.global_var()

if __name__ == '__main__':

    if(len(sys.argv) == 3):
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]

        g.n = arg1
        g.T = arg2
    else:
        g.n = 10


#What variables are important to take as an input?
#t, n, # locations to start with.

#Have core, and output chart.
#now just need input for users, then some form of mid program visual.

def init_people():

    for i in range(g.n):

        loc = {8:[1], 16:[2], 24:[3]}
        locs = list(g.locations)

        #number of times/location sets to have
        times = random.randint(1, 6)

        d = {}
        min_time = 1

        for ii in range(times):

            time_var = random.randint(min_time, 24)
            min_time = time_var

            num_place = random.randint(1, g.max_location)
            loc = random.sample(locs, num_place)

            d[time_var] = loc

            #END OF THE DAY REACHED, SLOPPYY
            if(time_var == 24):
                break

        immunity = random.randint(1, 100)

        #RIGHT NOW EVERYONE STARTS AT 1....

        lowest_time = min(d)
        starting_location = d[lowest_time][0]

        #ERROR AT STARTING_LOCATION RN
            
        #id, immunity, locations, response, current_location, sociability
        g.people.append(ci.node(i, immunity, d, 2, starting_location, 1))

        
def m():
    
    init_people()
    g.people[0].infected = 1
    
    for x in range(g.t):

        g.Current_Tick += 1
        
        #clear locations
        for i in g.locations.keys():
            g.locations[i] = []

        #build with list of individuals
        for i, person in enumerate(g.people):
            g.locations[person.current_location].append(i)

        #iterate through locations, and shuffle
        for i in g.locations.keys():
            random.shuffle(g.locations[i])

        #now, iterate through locations, and run pair test.
        #POTENTIAL ASYNC SECTION
        for i in g.locations.keys():
            current_location = g.locations[i]
            
            for ii, value in enumerate(current_location):
                a = current_location[ii]
                b = current_location[ii - 1]
                ci.pair_test(g.people[a], g.people[b], g)

        for i in g.people:
            ci.update_location(i, g)

        g.interacted[g.Current_Tick] = []

        for i in g.people:
            g.interacted[g.Current_Tick].append(i.interacted[:])

def user_input(arg1, arg2, arg3):
    
    x = 1



def calculate_weights():
    n = g.interacted

    people = {}
    min_interaction = 10
    max_interaction = 0
    edges = []
    weights = []

    #EQQQ DOUBLE NESTED LOOP WITH CONDITIONALS 
    for i in g.people:
    ##    people[i.id] = {}

        i.interacted.sort()

        for ii in i.interacted:

            x = min(i.id, ii)
            y = max(i.id, ii)

            if (x, y) in people:
                people[(x, y)] += 1
            else:
                people[(x, y)] = 1

            #BOOO UGLY CODE 
            if people[(x, y)] > max_interaction:
                max_interaction = people[(x, y)]
            if people[(x, y)] < min_interaction:
                min_interaction = people[(x, y)]

    max_min = max_interaction - min_interaction
        
    for i in people:
        
        weight = people[i]
        normalized_weight = ( max_interaction - weight ) / ( max_min ) * 100
        normalized_weight = round(normalized_weight, 1)
        edges.append(i)
        weights.append((i[0], i[1],normalized_weight))

    return(edges, weights)

def draw(edge_trace, node_trace):
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout = go.Layout(
                        showlegend=False,
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        
                    )
    return fig
##    plt.show()
##        fig.show()


def build_plotly():
    x=1

def save_json_output(output):
    d = output
    
    cc = {f"Node: {i}":round(d[5][i],2) for i in d[5]}
    dc = {f"Node: {i}":round(d[7][i],2) for i in d[7]}
    sh = {f"Node: {i}":round(d[9][i],2) for i in d[9]}
    ec = {f"Node: {i}":round(d[11][i],2) for i in d[11]}

    simulation_results = [{
        "Number of People":d[2],
        "Number of Infected":d[1],
        "Max infecter":d[12],
        "Number Dead":d[13]
        }
        ]

    network_analysis = [{
        "Number of Edges":d[3],
        "Graph Density":d[4],
        "Has Bridges":d[6],
        "Global Efficiency":round(d[8],2),
        "Wiener Index":d[10],
        "Closeness Centrality":cc,
        "Degree Centrality":dc,
        "Structural Holes":sh,
        "Eigenvector Centrality":ec
        }]

    data_output = [{
        "Number of People":d[2],
        "Number of Infected":d[1],
        "Number of Edges":d[3],
        "Graph Density":d[4],
        "Has Bridges":d[6],
        "Global Efficiency":round(d[8],2),
        "Wiener Index":d[10],
        "Max infecter":d[12],
        "Closeness Centrality":cc,
        "Degree Centrality":dc,
        "Structural Holes":sh,
        "Eigenvector Centrality":ec,
        "Number Dead":d[13]

        }]

    with open('test_output.json','w') as json_file:
           json.dump(data_output, json_file)

    with open('simulation_results.json','w') as json_file:
           json.dump(simulation_results, json_file)

    with open('network_analysis.json','w') as json_file:
           json.dump(network_analysis, json_file)

    

def main(arg1, arg2, arg3, arg4, arg5, arg6):

    g.n = int(arg1)
    g.T = int(arg2)
    g.people = []

    g.min_immunity = int(arg4)
    g.max_immunity = int(arg5)
    g.mortality_rate = int(arg6)
    
    m()

    edges, weights = calculate_weights()

    p = g.people
    x = ci.state_stats(g)
    infected_list = x[2]
    infected_by = x[3]
    people = []

    for i in range(len(g.people)):
        people.append(i)
            
    G = nx.Graph()
    G.add_weighted_edges_from(weights)
    pos = nx.spring_layout(G, seed=0)
    color_map = ['red' if node in infected_list else 'green' for node in G]
    nx.draw(G,pos,with_labels=True,node_color=color_map)

    pos = nx.random_layout(G)

    for i in pos:
        G.nodes[i].update({'pos':[pos[i][0],pos[i][1]]})

    edge_x = []
    edge_y = []
    node_x = []
    node_y = []

    #Assuming G.nodes has a position. Used for lines, 
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    #makes a series of scatter chart connections
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    healthy_color = 'rgb(21,248,255)'
    infected_color = 'rgb(49, 51, 95)'

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale = ((0.0, healthy_color),
                          (1.0, infected_color)),
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Infection Status',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    #Color nodes

    node_adjacencies = []
    node_text = []
    node_color = []

    #have some kind of normalization of node size
    for node, adjacencies in enumerate(G.adjacency()):
        other_data = g.people[node]
        node_adjacencies.append(len(adjacencies[1]) * 5)
        node_text.append(f"node {node}, # interactions: {str(len(adjacencies[1]))}\n"
                         +f"infected by node {other_data.infected_by} at {other_data.time_infected}"
                         + f"")

    #Make red if infected, green if healthy.
    for node in enumerate(G.nodes()):
        node_color.append(int(node[1] in infected_list))

    #change size based on number of connections
    node_trace.marker.color = node_color
    node_trace.text = node_text
    node_trace.marker.size = node_adjacencies

    fig = draw(edge_trace, node_trace)

    #maybe calculate who infected the most, etc.
    closeness_centrality = nx.closeness_centrality(G)
    bridges = nx.bridges(G)
    has_bridges = nx.has_bridges(G)
    degree_centrality = nx.degree_centrality(G)
    global_efficiency = nx.global_efficiency(G)
    #woah. Structural holes is cool. A concept that there can be gaps between
#two individuals with complementary setups, because of their connections connections
    structural_holes = nx.constraint(G)
    wiener_index = nx.wiener_index(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)
##    betweenness_centrality = nx.betweenness_centrality(G, weight=weights)

    #could implement isomorphic check if I tracked different graphs.
    #so, does one set of circumstances lead to the same outcomes as another?

    infected_by_arr = [0] * g.n
    num_infected = 0
    num_ppl = g.n
    num_edges = len(edges)
    dead = [0] * g.n
    num_dead = 0
    
    for i in g.people:
        infecter = i.infected_by

        if i.alive == 0:
            dead[i.id] = 1
            num_dead += 1

        if(infecter != -1):
            infected_by_arr[infecter] += 1
        if i.infected == 1:
            num_infected += 1

    max_infecter = max(infected_by_arr)

    max_infecter_id = infected_by_arr.index(max_infecter)

    graph_density = num_ppl / num_edges

    output = [infected_by_arr,
              num_infected,
              num_ppl,
              num_edges,
              graph_density,
              closeness_centrality,
              #bridges,
              has_bridges,
              degree_centrality,
              global_efficiency,
              structural_holes,
              wiener_index,
              eigenvector_centrality,
              max_infecter_id,
              num_dead
              ]

    print(output)
    
    fig.write_html("templates/plot.html")

##    with open('test_output.json','w') as json_file:
##           json.dump(x[2][5], json_file)

    save_json_output(output)

    return([G,fig,output])



    


##x = main(4,2,2, 10, 90, 1)
##G = x[0]
##dc = nx.degree_centrality(G)
##bc = nx.betweenness_centrality(G)
##edges, weights = calculate_weights()
####nx.betweenness_centrality(G,weight=weights)
##
##d = x[2]
##
##
##
##cc = {f"Node: {i}":round(d[5][i],2) for i in d[5]}
##dc = {f"Node: {i}":round(d[7][i],2) for i in d[7]}
##sh = {f"Node: {i}":round(d[9][i],2) for i in d[9]}
##ec = {f"Node: {i}":round(d[11][i],2) for i in d[11]}
##
##data_output = [{
##    "Number of People":d[2],
##    "Number of Infected":d[1],
##    "Number of Edges":d[3],
##    "Graph Density":d[4],
##    "Has Bridges":d[6],
##    "Global Efficiency":round(d[8],2),
##    "Wiener Index":d[10],
##    "Max infecter":d[12],
##    "Closeness Centrality":cc,
##    "Degree Centrality":dc,
##    "Structural Holes":sh,
##    "Eigenvector Centrality":ec,
##    "Number Dead":d[13]
##
##    }]
##
##with open('test_output.json','w') as json_file:
##       json.dump(data_output, json_file)

##with open('test_output.json','w') as json_file:
##       json.dump(x[2][5], json_file)




