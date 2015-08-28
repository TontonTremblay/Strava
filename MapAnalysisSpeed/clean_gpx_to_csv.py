import gpxpy
import gpxpy.gpx
import math
from haversine import haversine

def distance(p1,p2):
	return math.sqrt(((p1.latitude - p2.latitude) * (p1.latitude - p2.latitude) ) + 
		((p1.longitude - p2.longitude) * (p1.longitude - p2.longitude) ))


# Parsing an existing file:
# -------------------------

gpx_file = open('data.gpx', 'r')

gpx = gpxpy.parse(gpx_file)

data = []


for track in gpx.tracks:
    for segment in track.segments:
    	points = segment.points
    	for i in range(len(points)):
    		point = {}
    		point["coords"] = [points[i].latitude,points[i].longitude]
    		point["eval"] = points[i].elevation
    		point["time"] = points[i].time
    		data.append(point)

for i in range(len(data)):
	"""This assumes that the points are taken at every second"""
	#Should extend this to be more appropriate. 
	
	if i < len(data)-1:
		data[i]["distance_next"] = haversine(data[i]["coords"],data[i+1]['coords'])*1000
	else:
		data[i]["distance_next"] = 0.0

	if i>0:
		data[i]["distance_prev"] = haversine(data[i-1]["coords"],data[i]['coords'])*1000 
	else:
		data[i]["distance_prev"] = 0.0

	data[i]["vel_next_kms"] = data[i]["distance_next"] * 3.6
	data[i]["vel_prev_kms"] = data[i]["distance_prev"] * 3.6
