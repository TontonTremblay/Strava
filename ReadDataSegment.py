from stravalib.client import Client
import time

client = Client()



# token stored in a file

s = open("jtremblay.token")
l = s.readline()

client = Client(l)
athlete = client.get_athlete()


activities = client.get_activities()

athlete = client.get_athlete()


activities = client.get_activities(limit = 500)


c = 0

for act in activities:
	
	if c >30:
		c = 0
		time.sleep(60)
	c+=1	
	try:

		if act.type != "Ride": 
			continue
		data = client.get_activity(activity_id=act.id)

		print "+"
		print data.start_date
		for i in data.segment_efforts:
			name = i.name.encode('ascii',errors='ignore')
		
			# print name,i.id
			
			if name == "Camillien Houde":
				
				print i.moving_time		
	except:
		print "error"
		
a = client.get_activity(activity_id=276080785)
	# , include_all_efforts = True)

# print a.segment_efforts

# camilien houde, 6468199696




		





