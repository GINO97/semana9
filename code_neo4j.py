import pandas as pd
from py2neo import Graph

#get fight data
fights = pd.read_csv('D:/Big Data/dataset/ufc_peleas_hist.csv')
#ignore DQs
fights = fights[fights.method != 'DQ']

#connect to Neo4j graph (must have Neo4j running with default settings, password set to 123 or whatever you want)
graph = Graph(password="12345")

#load data into graph
tx = graph.begin()
for index, row in fights[fights.result == 'W'].iterrows():
    tx.evaluate('''
       MERGE (a: fighter {name: $fighter})
       MERGE (b: fighter {name: $opponent})
       MERGE (b)-[r:lose_to {date: $date, division: $division, method: $method}]->(a)
    ''', parameters = {'fighter': row['fighter'], 'opponent': row['opponent'], 'date':row['date'], 
                       'method':row['method'], 'division':row['division']})
tx.commit()