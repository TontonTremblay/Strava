""" 
    This file read the data created from ReadDataSegment.py or 
    any format. 
    It needs as argument a file name to read from. 
    It produces two graphs, the first one is named
    cloud_NAMEFILE.pdf represents the performance distribution
    of your segment over time. 
    The second graph, 
    dist_NAMEFILE.pdf is the probability distribution of all 
    your performances. A Gaussian is also plot over it. 
    Its title is  
"""



import time
import matplotlib.pyplot as plt
import datetime
import numpy as np
import matplotlib.dates as md
from scipy.stats import norm
import sys

# Comment this part if you do not want to use 
# the provided font
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

prop = fm.FontProperties(fname='FuturaLT.ttf')






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


try:
    fileName = sys.argv[1]
except:
    print "No name was given"
    # quit()
    fileName = "camillien_houde_JTremblay.data"
    print fileName

data = open(fileName)

fileName = fileName.replace(".data","")

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



#Used by the bins for the histogram
valuesFloat = [ float(s[2]+s[3])*60+float(s[5]+s[6]) for s in times]





#Find the holes in the data. Do something linear here. 

setData = []
j= 0
for i in range(len(dates)-1):
    if int(dates[i][5:7]) - int (dates[i+1][5:7]) > 0 :
        setData.append( [ dates[j:i+1],times[j:i+1]] )
        j = i+1

setData.append([dates[j:-1],times[j:-1]])


dataFinal = []

for v in setData:
    datesSub = v[0]
    timesSub = v[1]
    x = np.array([datetime.datetime(year = int(s[0:4]),
        month = int(s[5:7]),
        day = int(s[8:10])) for s in datesSub])

    y = np.array([datetime.datetime(year = 1,month = 1,day = 1, 
        hour = 1,minute = int(s[2]+s[3]), second = int(s[5]+s[6])) for s in timesSub])
    dataFinal.append([x,y])









# print x
# print y
plt.figure(1)

# sub = plt.subplot(211)
plt.plot(x,y,"yo",color="#0040ff",alpha =0.7)

fig,(ax,ax2) = plt.subplots(2,1,sharey=True)




# plt.gcf().autofmt_xdate()

# ax=plt.gca()


# # ax.set_xticklabels(ax.xaxis.get_majorticklocs(), fontproperties=prop)
# ax.set_yticklabels(ax.yaxis.get_majorticklocs(), fontproperties=prop)


# yfmt = md.DateFormatter('%M:%S')

# ax.yaxis.set_major_formatter(yfmt)


# ax.set_xlabel("Months",fontproperties=prop)
# ax.set_ylabel("Performance in M:S",fontproperties=prop)
# plt.gcf().autofmt_xdate()




# plt.title("Performance over time for "+ fileName.replace("_"," ") +" segment" ,fontproperties=prop)
# plt.show()


# plt.savefig("Cloud"+"_"+fileName+".pdf")













# DIFFERENT DATA


plt.clf()


plt.figure(1)




plt.hist(  valuesFloat, bins=25, normed=1, color = '#00A0ff',alpha=0.7)

mu, std = norm.fit(valuesFloat)
med = np.median(valuesFloat)

xmin, xmax = plt.xlim()

x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=1.4,color='#0040ff')
plt.axvline(med, color='#101010', linestyle='--', linewidth=1.3)
plt.axvline(mu, color= '#101010', linestyle='-.', linewidth=1.3)

plt.title("avg(--): " + str(time.strftime('%M:%S',time.gmtime(mu))) + 
    ", std: " + str(time.strftime('%M:%S',time.gmtime(std))) + 
    ", med(-.): " + str(time.strftime('%M:%S',time.gmtime(med))) + 
    ", n: "+ str(len(times)),fontproperties=prop)




ax=plt.gca()


# for v in ax.xaxis:
#   r.append(time.strftime('%M:%S',time.gmtime(v)))
# ax.xaxis = r
# ax.xaxis.set_major_formatter(md.DateFormatter('%M:%S'))

x = np.linspace(xmin, xmax, 10)

newx = []


for i in x:
    newx.append(time.strftime('%M:%S',time.gmtime(i)))


ax=plt.gca()

values = ax.xaxis.get_majorticklocs()


labels2 = []
for v in values:
    labels2.append(time.strftime('%M:%S',time.gmtime(v)))

ax.set_yticklabels(ax.yaxis.get_majorticklocs(), fontproperties=prop)
ax.set_xticklabels(labels2,fontproperties=prop)
ax.set_xlabel("Time in M:S",fontproperties=prop)
myFmt = md.DateFormatter('%S')
# ax.xaxis.set_major_formatter(myFmt)
plt.gcf().autofmt_xdate()

# plt.show()
# plt.savefig("Dist"+"_"+fileName+".pdf")
