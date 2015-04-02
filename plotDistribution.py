import time
import matplotlib.pyplot as plt
import datetime
import numpy as np
import numpy
import matplotlib.dates as md
from scipy.stats import norm

def isTimeFormat(input):
    try:
        time.strptime(input, "%H:%M:%S")
        return True
    except ValueError:
        return False

def isDay(input):
    try:
        time.strptime(input, "%Y-%m-%d")
        return True
    except ValueError:
        return False



data = open("Camilien-houde2.txt")

times = []
dates = []
date = ""

# print isDay("2013-06-05")

for i in data:

	if isDay( i[0:10] ) :
		date = i[0:10]
		# print date
	i = str(i).replace("\n","")
	if isTimeFormat(i):
		times.append(i)
		dates.append(date)
		# print date

# print times	

times = list(reversed(times))
dates = list(reversed(dates))

# s= "2013-06-05"
# print int(s[0:4])
# print int(s[5:7])
# print int(s[8:10])

x = np.array([datetime.datetime(year = int(s[0:4]),
	month = int(s[5:7]),
	day = int(s[8:10])) for s in dates])

y = np.array([datetime.datetime(year = 1,month = 1,day = 1, 
	hour = 1,minute = int(s[2]+s[3]), second = int(s[5]+s[6])) for s in times])

# print x
# print y
plt.figure(1)
# sub = plt.subplot(211)
plt.plot(x,y,"yo",color="#0040ff",alpha =0.7)
# plt.gcf().autofmt_xdate()

ax=plt.gca()

yfmt = md.DateFormatter('%M:%S')
ax.yaxis.set_major_formatter(yfmt)
ax.set_xlabel("Months")
ax.set_ylabel("Performance in M:S")
plt.gcf().autofmt_xdate()
# ax.xaxis.tick_top()

valuesFloat = [ float(s[2]+s[3])*60+float(s[5]+s[6]) for s in times]

plt.title("Distribution of performance over time")
# plt.show()
plt.savefig("Cloud.pdf")


# DIFFERENT DATA


plt.clf()


plt.figure(1)




plt.hist(  valuesFloat, bins=25, normed=1, color = '#00A0ff',alpha=0.7)

mu, std = norm.fit(valuesFloat)
med = numpy.median(valuesFloat)

xmin, xmax = plt.xlim()

x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=1.4,color='#0040ff')
plt.axvline(med, color='#101010', linestyle='--', linewidth=1.3)
plt.axvline(mu, color= '#101010', linestyle='-.', linewidth=1.3)

plt.title("avg(--): " + str(time.strftime('%M:%S',time.gmtime(mu))) + 
	", std: " + str(time.strftime('%M:%S',time.gmtime(std))) + 
	", med(-.): " + str(time.strftime('%M:%S',time.gmtime(med))) + 
	", n: "+ str(len(times)))




ax=plt.gca()


# for v in ax.xaxis:
# 	r.append(time.strftime('%M:%S',time.gmtime(v)))
# ax.xaxis = r
# ax.xaxis.set_major_formatter(md.DateFormatter('%M:%S'))

x = np.linspace(xmin, xmax, 10)

newx = []


for i in x:
	newx.append(time.strftime('%M:%S',time.gmtime(i)))


ax=plt.gca()

values = [i for i in range(300,701,50)]

print values

labels = dict()
labels2 = []
for v in values:
	labels[v] = time.strftime('%M:%S',time.gmtime(v))
	labels2.append(time.strftime('%M:%S',time.gmtime(v)))

ax.set_xticklabels(labels2)
ax.set_xlabel("Time in M:S")
myFmt = md.DateFormatter('%S')
# ax.xaxis.set_major_formatter(myFmt)
plt.gcf().autofmt_xdate()

# plt.show()
# plt.savefig("dist.pdf")
