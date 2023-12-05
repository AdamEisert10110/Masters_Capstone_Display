import random
import networkx as nx
import matplotlib.pyplot as plt
import pdb
import matplotlib.pyplot as plt
import plotly.graph_objects as go

random.seed(0)

class global_var:
    
    people = []                         #list of all people
    n = 10                              #number of people
    t = 3                              #t is the time period
    locations = {1:[], 2:[], 3:[]}      #list of locations
    max_location = 3                    #max num of locations
    max_immunity = 1                    #max level of immunity, 1-99, %catch
    min_immunity = 1
    interacted = {}
    Current_Tick = 1
    mortality_rate = 1                  #Odds of causing dead, 1-1000

class disease:
    
    def __init__(self, _type, fatality, incubation, symptoms, exposure):
        self._type = _type
        self.death = fatality
        self.incubation = incubation
        self.exposure = exposure

class node:

    infected = 0
    time_infected = 0
    visible_infection = 0
    infected_by = -1
    location_infected = 0
    alive = 1

    def __init__(self, _id, immunity,
                 locations, response,
                 current_location, sociability):

        self.id = _id
        self.immunity = immunity
        self.location = locations
        self.response = response
        self.current_location = current_location
        self.sociability = sociability  #number of ppl they'll interact with
        self.interacted = []

def pair_test(a, b, g):

    infected = 1
##    min_risk = 1
##    max_risk = 100

    min_risk = max(g.min_immunity, 1)
    max_risk = min(g.max_immunity, 100)
    
    a_infected = a.infected
    b_infected = b.infected
    a_immunity = a.immunity
    b_immunity = b.immunity

    #pdb.set_trace()
    if b.id != a.id:
        a.interacted.append(b.id)
    
    #no one is infected, or both are infected, no operation occurs
    if(a_infected == b_infected):
        return
 
    #run test for infection
    infection = random.randint(min_risk, max_risk)
  
    #checks if threshold for infection is not met, exits if not.
    if((a_infected != infected and a_immunity > infection)
       or (b_infected != infected and b_immunity > infection)):
        return

    #infection successful, there will be transference.
    if(a_infected != infected):
        a.infected_by = b.id
        a.time_infected = g.Current_Tick
        a.location_infected = a.current_location

    if(b.infected != infected):
        b.infected_by = a.id
        b.time_infected = g.Current_Tick
        b.location_infected = b.current_location

    #check for mortality.
    a_mortality = random.randint(1, 1000)
    b_mortality = random.randint(1, 1000)

    if a_mortality < g.mortality_rate:
        a.alive = 0

    if a_mortality < g.mortality_rate:
        b.alive = 0
        
        
    a.infected = 1
    b.infected = 1

    return


#IF HOURS ARE NOT IN ASCENDING ORDER THIS WILL BREAK
def update_location(a, g):

    Time_Unit = g.Current_Tick % 24
    a_loc = a.location
    location_change_time = a_loc.keys()
    locations = a_loc.values()

    #IS THIS THE BEST THING TO USE? NOOOO
    for i, value in enumerate(location_change_time):
        if(value >= Time_Unit):
            location_choice = a_loc[value]
            random.shuffle(location_choice)
            a.current_location = location_choice[0]

            break
    return

def state_check(g):

    total_people = len(g.people)
    total_infected = 0
    infected_list = []
    infected_by = []
    infected_location = []
    infected_time = []
    
    for person in g.people:
        
        if(person.infected):
            total_infected += 1
            infected_list.append(person.id)
            infected_by.append(person.infected_by)
            infected_time.append(person.time_infected)
            infected_location.append(person.location_infected)

    state = "\nSTATE\n----------------"
    state +=f"\nCurrent_Tick: {g.Current_Tick}"
    state +=f"\nTotal Infected: {total_infected}"
    state +=f"\nPercent Infected: {total_infected / total_people * 100}"
    state +=f"\nInfected List: {infected_list}"
    state +=f"\nInfected By: {infected_by}"
    state +=f"\nInfected Time: {infected_time}"
    state +=f"\nInfected Location: {infected_location}"
    
    return state

#dusplicated code, booooo
def state_stats(g):

    total_people = len(g.people)
    total_infected = 0
    infected_list = []
    infected_by = []
    infected_location = []
    infected_time = []
    
    for person in g.people:
        
        if(person.infected):
            total_infected += 1
            infected_list.append(person.id)
            infected_by.append(person.infected_by)
            infected_time.append(person.time_infected)
            infected_location.append(person.location_infected)
    
    return [total_infected, total_people, infected_list,
            infected_by, infected_time, infected_location]

#GRAPHINH, FOR POST EXECUTION

def graph_infected(g):

    x = state_stats(g)
    infected_list = x[2]
    infected_by = x[3]

    edges = []

    for i, val in enumerate(infected_by):
        if val > -1:
            infectee = infected_list[i]
            edges.append((val, infectee))
        
    
    G = nx.Graph()

    G.add_nodes_from(infected_list)
    G.add_edges_from(edges)
    nx.draw(G,with_labels=True)
    plt.show()

def graph_total(g):
    edges = []
    p = g.people

    x = state_stats(g)
    infected_list = x[2]
    infected_by = x[3]
    people = []

    for i in range(len(g.people)):
        people.append(i)

    for i in p:
        for ii in i.interacted:
            x = min(i.id, ii)
            y = max(i.id, ii)
            new_edge = (x, y)

            if new_edge not in edges and new_edge not in edges:
                edges.append(new_edge)
            
    G = nx.Graph()

    G.add_nodes_from(people)
    G.add_edges_from(edges)
    color_map = ['red' if node in infected_list else 'green' for node in G]
    nx.draw(G,with_labels=True,node_color=color_map)
    plt.show()
    

def graph_total_infected_connected(g):
    x = state_stats(g)
    infected_list = x[2]
    infected_by = x[3]
    people = []

    for i in range(len(g.people)):
        people.append(i)

    edges = []


    for i, val in enumerate(infected_by):
        if val > -1:
            infectee = infected_list[i]
            edges.append((val, infectee))
            
    G = nx.Graph()

    G.add_nodes_from(people)
    G.add_edges_from(edges)
    color_map = ['red' if node in infected_list else 'green' for node in G]
    nx.draw(G,with_labels=True,node_color=color_map)
    plt.show()
    

#test of graphing capabilities
#MIGHT HAVE TO OVERHAUL GRAPHING TO BE MORE LIKE GRAPH_TOTAL,
#SET UP X,Y WITH MIN,MAX, THEN SEE IF IT EXISTS BEFORE PLACING INTO EDGE.
def graph_test_1(g):

    #displays grpah of infections
    G = nx.Graph()
    G.add_node(1)
    G.add_nodes_from([(2,{"color":"red"})
                      ,3])
    G.add_edge(1,2)
    G.add_edge(2,3)

    G.clear()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    e = [(1,8), (2,0), (3,7), (4,0), (5,2), (6,3), (7,0), (8,0), (9,7)]
    G.add_edges_from(e)
    
    nx.draw(G,with_labels=True)
    plt.show()

def plotly_chart(g):

    #code for post modeling graph creation and analysis.
    #some form of total mapping is required.
    #tracking when each point of contact was made, and the users state at the time.
    #can add alterations for unit size, alone time, transport, etc.

    #post simulation graph....
    #we can have weights on a scale from 1-100,
    #with lower weights for more interactions.
    #Starts at 100, then with each interaction, reduce by 10? or t * factor
    #note to self, to append a uni

    #makes count of who has interacted with who
    #can use this as a weight

    n = g.interacted

    people = {}
    min_interaction = 10
    max_interaction = 0

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

            
    #After count of interactions is made, with min and max to normalize,
    #go thru, normalize the data, then display graph with edges.


    #except, more interactions should decrease weight, to show how
    #easy it is for the disease to rip thru
    #so we invert the (x - xmax) / (xmax - xmin)

    max_min = max_interaction - min_interaction
        
    edges = []
    weights = []

    for i in people:
        
        weight = people[i]

        normalized_weight = ( max_interaction - weight ) / ( max_min ) * 100

        normalized_weight = round(normalized_weight, 1)

        edges.append(i)
        weights.append((i[0], i[1],normalized_weight))

    p = g.people
    x = state_stats(g)
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

    #generic code
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    #Color nodes

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    #Create network graph

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.show()

    

##def graphics_test():
##    pygame.init()
##    # Set up the drawing window
##    screen = pygame.display.set_mode([500, 500])
##    # Run until the user asks to quit
##    running = True
##    while running:
##        # Did the user click the window close button?
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                running = False
##        # Fill the background with white
##        screen.fill((255, 255, 255))
##        # Draw a solid blue circle in the center
##        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
##        # Flip the display
##        pygame.display.flip()
##    # Done! Time to quit.
##    pygame.quit()

