#Packages needed for triangle arb
import json, urllib.request, sys, math, re
import numpy as np

import os
from twilio.rest import Client
from dotenv import load_dotenv

#packages needed for integration
from plyer import notification


#empty list and dic to properly graph endpoints
graph = {}
paths = []



#main function
def main():
    submit = []
    forex_rates = get_rates()
    print("Current Forex Rates:")
    print(forex_rates)
    print("\n")
    gr = get_graph(forex_rates)
    
    for key in graph:
        path = bellman_ford(graph, key)
        if path not in paths and not None:
            paths.append(path)

    for path in paths:
        if path == None:
            print("No Arbitrage opportunity detected in current rates :(")
        else:
            money = 100
            
            notification.notify(title= "<---Arbitrage cycle detected--->",
                    message= "Starting with %(money)i in %(currency)s" % {"money":money,"currency":path[0]},
                    app_icon = None,
                    timeout= 1,
                    toast=False)

            #Twilio and Desktop integration
            load_dotenv() 
            #Twilio Auth Key needs to be reset periodically       
            account_sid = 'ACcd99d0ef7c6e5a8788f01331229a6bae'
            auth_token = '5053df8cd52ff48b52877bc169b35e07'
            #account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            #auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            print(account_sid, auth_token)
            client = Client(account_sid, auth_token)

            # # message = client.messages \
            #             .create(
            #              body="Arbitrage Oppurtunity Found!",
            #             from_='+19416134207',
            #             to='+16467966700'
            #             )

            print("<---Arbitrage cycle detected--->")
            print("Starting with %(money)i in %(currency)s" % {"money":money,"currency":path[0]})

            for i,value in enumerate(path):
                if i+1 < len(path):
                    start = path[i]
                    end = path[i+1]
                    rate = math.exp(-graph[start][end])
                    money *= rate
                    print("%(start)s to %(end)s at a rate of %(rate)f = %(money)f" % {"start":start,"end":end,"rate":rate,"money":money})
                    a = "%(start)s to %(end)s at a rate of %(rate)f = %(money)f" % {"start":start,"end":end,"rate":rate,"money":money}
                    submit.append(a)
                    
        print("\n")

    return submit




#getting the rates 
def get_rates():
    try:
        forex_url = urllib.request.urlopen("http://fx.priceonomics.com/v1/rates/")
        forex_r = forex_url.read()
        rates = json.loads(forex_r)
    except Exception as e:
        print >>sys.stderr, "Error getting rates:", e
        sys.exit(1)
    
    return rates


#getting the graph
def get_graph(forex_rates):
    pattern = re.compile("([A-Z]{3})_([A-Z]{3})")
    for key in forex_rates:
        matches = pattern.match(key)
        conversion_rate = -math.log(float(forex_rates[key]))
        from_rate = matches.group(1)
        to_rate = matches.group(2)
        if from_rate != to_rate:
            if from_rate not in graph:
                graph[from_rate] = {}
            graph[from_rate][to_rate] = float(conversion_rate)
    return graph

#init paths
def initialize(graph, source):
    d = {} # Stands for destination
    p = {} # Stands for predecessor
    for node in graph:
        d[node] = float('Inf') # We start admiting that the rest of nodes are very very far
        p[node] = None
    d[source] = 0 # For the source we know how to reach
    return d, p    

#bellford #1
def relax(node, neighbor, graph, d, p):
    # If the distance between the node and the neighbor is lower than the one I have now
    if d[neighbor] > d[node] + graph[node][neighbor]:
        # Record this lower distance
        d[neighbor]  = d[node] + graph[node][neighbor]
        p[neighbor] = node    


#retrace function
def retrace_negative_loop(p, start):
    arbitrageLoop = [start]
    next_node = start
    while True:
        next_node = p[next_node]
        if next_node not in arbitrageLoop:
            arbitrageLoop.append(next_node)
        else:
            arbitrageLoop.append(next_node)
            arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
            return arbitrageLoop


#bellman_final
def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            for v in graph[u]: #For each neighbor of u
                relax(u, v, graph, d, p) #Lets relax it


    # Step 3: check for negative-weight cycles
    for u in graph:
        for v in graph[u]:
            if d[v] < d[u] + graph[u][v]:
                return(retrace_negative_loop(p, source))
    return None





#main function 
if __name__ == '__main__':
  a = main()   
  print(a)   
