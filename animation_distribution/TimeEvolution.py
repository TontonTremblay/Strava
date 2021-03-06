import csv
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from pylab import *
import seaborn as sns
import pandas as pd
import time 
import subprocess
sns.set(style="white", palette="muted", color_codes=True)
import os

directory = "output/"

f = open("camillien_houde_JTremblay.data")
data = []
day = None
for i in f:
    if "-" in i:
        # day = time.strptime(i[0:10].replace("-"," "),"%Y %m %d")
        day = i[0:10].replace("-","/")
    else: 
        # performance = time.strptime(i.replace("\n",""),"%H:%M:%S")
        performance = i.replace("\n","")
        p = pd.Timestamp(performance)
        data.insert(0,[pd.to_datetime(day),day[0:4],day[5:7],day[8:],p.minute * 60 + p.second])

f.close()    




df = pd.DataFrame(data,columns=["date", "year","month","day","performance (s.)"])

# df = df.iloc[::-1]

length =  df.count()["date"]-1
# print df
# quit()


start = 10
i = 0 
j = start
interval = 30

maxValue = []
sns.despine()

years = df.year.unique()

#personal records saved per year
prs = {}

for y in years:
    prs[y] = "inf"

    if not os.path.exists(directory+y):
        os.makedirs(directory+y)
 
c = 0



#This is the year long animation
while 1:
    break
    if i >= length-start:
        break
    elif  j-i < interval and j<length:
        j+=1
    else:
        i+=1
        if j<length:
            j+=1
    
    if j is length:
        j -=1

    dft = df[i:j]
    ax  = sns.distplot(dft["performance (s.)"],hist=False,rug=True, color="r")
    maxValue.append( sns.plt.axis()[3])
    # sns.kdeplot(dft["performance (s.)"], bw=2, label="bw: 2")

    sns.plt.axvline(dft["performance (s.)"].median(), color='#101010', linestyle='--', linewidth=1.3,alpha=0.5)
    # sns.plt.axvline(dft["performance (s.)"].mean(), color= '#101010', linestyle='-.', linewidth=1.3)
    
    d1 = str(df["date"][i].year) + "/" + str(df["date"][i].month).zfill(2) + "/" + str(df["date"][i].day).zfill(2)
    d2 = str(df["date"][j].year) + "/" + str(df["date"][j].month).zfill(2) + "/" + str(df["date"][j].day).zfill(2)

    ax.annotate(d1 + " to " + d2,ha="left",xy=(550,0.0112))
    

    #Mention that a new season started
    if not d1[3] in d2[3]:
        ax.annotate("New season",size="small",xy = [307,0.0113] )
        # print "hello"
    ax.annotate(time.strftime('%M:%S',time.gmtime(dft["performance (s.)"].median())), size="small",ha="left",xy=(dft["performance (s.)"].median()+7,0.0014))


    #Write the pr
    pos_y = 0.00045
    for k in sorted(prs.keys()):
        s =  dft[dft["year"] == k]["performance (s.)"]     
        #Update the personal best
        if not s.count() == 0:
            m = min (s)
            if prs[k] > m:
                prs[k] = m 
        ax.annotate("Personal Best (year)", size="small",ha="left",xy=(553,0.0103))

        if not prs[k] is 'inf':
            ax.annotate(k + ": " + time.strftime('%M:%S',time.gmtime(prs[k])), size="small",ha="left",xy=(560,0.0103 - pos_y))
        pos_y += 0.00045



    sns.plt.axis([300, 700, 0, 0.012])
    

    #set the values in minutes
    values = ax.xaxis.get_majorticklocs()
    labels2 = []
    for v in values:
        labels2.append(time.strftime('%M:%S',time.gmtime(v)))

    ax.set_xticklabels(labels2)
    sns.plt.title("Performance distribution (interval of "+ str(interval) +" days)\n (doted line is the interval median)")
    ax.set_xlabel("Perfomance (minutes : seconds)")
    ax.set_ylabel("Distribution (percent)")
    c+=1
    sns.plt.savefig("output/all/"+str(c).zfill(3)+".png")
    # sns.plt.show()
    sns.plt.clf()
    # break
# print max(maxValue)        
    

    # quit()

#All the data


#Data per year
for k in sorted(prs.keys()):
    # break
    s =  df[df["year"] == k]     
    
    

    sns.set(style="white", palette="muted", color_codes=True)
    ax = sns.distplot(s["performance (s.)"], hist=False, rug=True, color="r")
    sns.plt.axvline(s["performance (s.)"].median(), color='#101010', linestyle='--', linewidth=1.3,alpha=0.5)
    ax.annotate(time.strftime('%M:%S',time.gmtime(s["performance (s.)"].median())), size="small",ha="left",xy=(s["performance (s.)"].median()+7,0.0014))

    sns.plt.axis([300, 700, 0, 0.012])


    #set the values in minutes
    values = ax.xaxis.get_majorticklocs()
    labels2 = []
    for v in values:
        labels2.append(time.strftime('%M:%S',time.gmtime(v)))

    ax.set_xticklabels(labels2)
    sns.plt.title("distribution performance in " + k + " n = "+str(s.count()["date"])+"\n (Dashed line is the median)")
    
    ax.set_xlabel("Perfomance (minutes : seconds)")
    ax.set_ylabel("Distribution (percent)")

    sns.plt.savefig("output/dist_"+k+".png")
    sns.plt.clf()
    # sns.plt.show()


    #Create an animation of the year
    i = 0
    j = 1
    interval = 30 
    length = s.count()["date"]-1
    c = 0


    timeData = []
    for r in s.iterrows():
        timeData.append(r)
    # print timeData
    while 1:
        break
        if i >= length-10:
            break
        elif  j-i < interval and j<length:
            j+=1
        else:
            i+=1
            if j<length:
                j+=1
        
        if j is length:
            j -=1


        dft = s[i:j]
        
        # print timeData[i][1]["date"]
        # print s
        # print dft[45].day
        # print dft[46].day
        # quit()
        ax  = sns.distplot(dft["performance (s.)"],hist=False,rug=True, color="r")
        maxValue.append( sns.plt.axis()[3])
        # sns.kdeplot(dft["performance (s.)"], bw=2, label="bw: 2")

        sns.plt.axvline(dft["performance (s.)"].median(), color='#101010', linestyle='--', linewidth=1.3,alpha=0.5)
        # sns.plt.axvline(dft["performance (s.)"].mean(), color= '#101010', linestyle='-.', linewidth=1.3)
        
        d1 = str(timeData[i][1]["year"]) + "/" + str(timeData[i][1]["month"]).zfill(2) + "/" + str(timeData[i][1]["day"]).zfill(2)
        d2 = str(timeData[j][1]["year"]) + "/" + str(timeData[j][1]["month"]).zfill(2) + "/" + str(timeData[j][1]["day"]).zfill(2)

        ax.annotate(d1 + " to " + d2,ha="left",xy=(550,0.0112))
        

        #Mention that a new season started
        if not d1[3] in d2[3]:
            ax.annotate("New season",size="small",xy = [307,0.0113] )
            # print "hello"
        ax.annotate(time.strftime('%M:%S',time.gmtime(dft["performance (s.)"].median())), size="small",ha="left",xy=(dft["performance (s.)"].median()+7,0.0014))



        performances =  min(dft[dft["year"] == k]["performance (s.)"])     
        ax.annotate("Personal Best", size="small",ha="left",xy=(553,0.0103))

        ax.annotate(time.strftime('%M:%S',time.gmtime(performances)), size="small",ha="left",xy=(560,0.0098))
        #     pos_y += 0.00045



        sns.plt.axis([300, 700, 0, 0.012])
        

        #set the values in minutes
        values = ax.xaxis.get_majorticklocs()
        labels2 = []
        for v in values:
            labels2.append(time.strftime('%M:%S',time.gmtime(v)))

        ax.set_xticklabels(labels2)
        ax.set_xlabel("Perfomance (minutes : seconds)")
        ax.set_ylabel("Distribution (percent)")
        
        # print "output/"+k+"/"+str(c).zfill(3)+".png"
        sns.plt.savefig("output/"+k+"/"+str(c).zfill(3)+".png")
        sns.plt.title(k)
        c+=1
        # sns.plt.show()  
        sns.plt.clf()
        # break
    # break




# subprocess.call(['output/animate.sh'])

sns.set(style="white", palette="muted", color_codes=True)
ax = sns.distplot(df["performance (s.)"], hist=False, rug=True, color="r")
sns.plt.axvline(df["performance (s.)"].median(), color='#101010', linestyle='--', linewidth=1.3,alpha=0.5)
ax.annotate(datetime.timedelta(seconds= df["performance (s.)"].median()), size="small",ha="left",xy=(df["performance (s.)"].median()+7,0.0014))

#set the values in minutes
values = ax.xaxis.get_majorticklocs()
labels2 = []
for v in values:
    labels2.append(time.strftime('%M:%S',time.gmtime(v)))

ax.set_xticklabels(labels2)
sns.plt.title("Distribution performance all, n = "+str(df.count()["date"])+"\n (Dashed line is the median)")

ax.set_xlabel("Perfomance (minutes : seconds)")
ax.set_ylabel("Distribution (percent)")

sns.plt.savefig("output/allDist.png")

# sns.plt.show()





