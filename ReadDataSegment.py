""" This code connects to a Strava client, download all of his activities
	and reads all of his segments. In order to work well the code 
	needs two string as input. A third optionnal argument can be passed 
	to mentionned how many max you want the program to look at.  

	(1) first input: The user has to provide a token stored in a text file; 
	the token is provided by strava, please refer to the following website
	http://pythonhosted.org/stravalib/usage/auth.html#requesting-authorization
	
	(2) second input is the segment the user is interested in downloading. 

	With all the data the code will write to a text file the date of the 
	performance and followed by all the performances for that date 
	(minute:second).
	If you interested in ploting that information, please refer to 
	PlotDistribution.py

	N.B. Since Strava limits the number of query a program can make to 
	600 requests every 15 minutes, 30000 daily, I added a sleep one 
	minute for every set of 30 queries. Hence this program 
	might feel slow.  

	Jonathan Tremblay, jtremblay@cs.mcgill.ca
"""


import time
import sys

try:
	token = sys.argv[1]
	segmentName = sys.argv[2].lower()

except:
	print "Error, missing inputs"
	quit()

# This is for the optional argument
limitActivities = 500



try:
	limitActivities = int(sys.argv[3])
except:
	print "limit of activities is",limitActivities




s = open(token)
l = s.readline()
s.close()

#Strava stuff
from stravalib import Client


client = Client(l)
athlete = client.get_athlete()
athleteName = athlete.firstname+athlete.lastname
print "Athlete",athlete.firstname,athlete.lastname


activities = client.get_activities(limit = limitActivities)

# The output data is stored in a string to be 
# stored in a text file
dataOutput = "" 

c = 0

print "looking for segment",segmentName

for act in activities:
	
	if c >30:
		c = 0
		time.sleep(60)
	c+=1	
	try:

		if act.type != "Ride": 
			continue
		data = client.get_activity(activity_id=act.id)


		dataOutput+= str(data.start_date) + '\n'
		
		for i in data.segment_efforts:
			name = i.name.encode('ascii',errors='ignore')
			name = name.lower()		
			# print name, segmentName

			if name == segmentName:
				
				dataOutput+= str(i.moving_time) + "\n"		
	except:
		print "error, might be too many query or activity private."

# Write to a file

# print dataOutput
segmentName=segmentName.replace(" ","_")
f = open(segmentName+"_"+athleteName+".data","w")
f.write(dataOutput)
f.close()		





