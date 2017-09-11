
import pandas as pd
import networkx as nx
import pylab

# Load trip data file and convert it to a dictionary of lists
df = pd.read_csv('trip.csv')
headers = list(df)
rows = df.values.tolist()
columns = list(map(list, zip(*rows)))
data = dict()
for i, header in enumerate(headers):
	data[header] = columns[i]

# Get unique station ids
unique_stations = []
for station_id in data['start_station_id']:
	if station_id not in unique_stations:
		unique_stations.append(station_id)
for station_id in data['end_station_id']:
	if station_id not in unique_stations:
		unique_stations.append(station_id)

# Count trips between stations
counts = dict()
for start_id in unique_stations:
	for end_id in unique_stations:
		counts[(start_id, end_id)] = 0
for i in range(len(data['start_station_id'])):
	start_id = data['start_station_id'][i]
	end_id = data['end_station_id'][i]
	counts[(start_id, end_id)] += 1

# Create network
G = nx.DiGraph()
for start_id in unique_stations:
	for end_id in unique_stations:
		G.add_edge(start_id, end_id, weight = counts[(start_id, end_id)])

# Visualize
nx.draw_networkx(G)
pylab.show()