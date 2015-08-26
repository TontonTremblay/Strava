import csv
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle
from pylab import *
import seaborn as sns
import pandas as pd
import time 
import subprocess
sns.set(style="white", palette="muted", color_codes=True)
import os
import random 
import copy

# from lmfit import Model
from scipy.interpolate import spline





def CreateGraphIntervalDates(df,d0,d1,c=None,folder=None,name=None):

    if c is None:
        c = "all"

    #try to make a 1d heat map
    # fig = plt.figure(0)
    gs = matplotlib.gridspec.GridSpec(2, 1, height_ratios=[1, 5],hspace=0.05)

    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    # print ax
    # gs.tight_layout(fig)



    # This creates the first plot. We are interested in showing 
    # a cloud distribution of the points. 

    x = np.array(df["date"])
    y = np.array(df["performance (s.)"])
    ax1.plot(x,y,"o")


    start, end = ax1.get_ylim()

    labels = ax1.get_yticks().tolist()


    for i in range(len(labels)):
        if i % 2 is 1:
            labels[i] = ""
        else:
            labels[i] = time.strftime('%M:%S',time.gmtime(labels[i]))
    labels[0]=""


    # a = np.arange(start, end, len(labels)))

    ax1.set_yticklabels(labels)


    ax1.xaxis.tick_top()

    num_days = d1 - d0
    # print num_days    
    ax1.add_patch(Rectangle( (d0,start),num_days.days,end,facecolor='gray',alpha = 0.3 ))

    # ax1.xlabel(verticalalignment="top")
    ax1.set_ylabel("performance (m:s)")

    # print df

    mask = (df['date'] >= d0) & (df['date'] <= d1)
    

    dft = df.loc[mask]

    # return

    ax1.set_title("Distribution performances, n = "+
        str(dft["date"].count()),y = 1.35)

    # test single entries
    # st = df.ix[random.sample(dft.index, 1)]
    # dft = st
    # print type(dft)

    
    empty = False 
    
    if dft.empty :
        empty = True
        day = pd.Timestamp(pd.to_datetime("2000-01-01"))
        dft = pd.DataFrame([[day,"","","","",20000,-1],[day,"","","","",2000,-1]],columns=["date", "date_text","year","month","day","performance (s.)","id"])
        

    if int(dft["date"].count()) == 1:

        st = list(dft.iloc[0])
        # print st 

        st1 = copy.copy(st)
        st1[5] = st[5]+1
        dft = pd.DataFrame([st,st1],columns=["date", "date_text","year","month","day","performance (s.)","id"])


    #Second part of the plot
    timeData = []
    for r in df.iterrows():
        timeData.append(r)




    ax  = sns.distplot(dft["performance (s.)"],hist=False,rug=True, color="b",ax=ax2)
    maxValue.append( sns.plt.axis()[3])
    # sns.kdeplot(dft["performance (s.)"], bw=2, label="bw: 2")

    sns.plt.axvline(dft["performance (s.)"].median(), color='#101010', linestyle='--', linewidth=1.3,alpha=0.5)
    # sns.plt.axvline(dft["performance (s.)"].mean(), color= '#101010', linestyle='-.', linewidth=1.3)
    
    # date_interval_1 = str(timeData[pos0][1]["year"]) + "/" + str(timeData[pos0][1]["month"]).zfill(2) + "/" + str(timeData[pos0][1]["day"]).zfill(2)
    # date_interval_2 = str(timeData[pos1][1]["year"]) + "/" + str(timeData[pos1][1]["month"]).zfill(2) + "/" + str(timeData[pos1][1]["day"]).zfill(2)

    ax.annotate(str(d0.strftime('%Y-%m-%d'))+ " to " + str(d1.strftime('%Y-%m-%d')),ha="left",xy=(550,0.0112))
    

    #Mention that a new season started

    # if not d1[3] in d2[3]:
    #     ax.annotate("New season",size="small",xy = [307,0.0113] )
        # print "hello"
    
    ax.annotate(time.strftime('%M:%S',time.gmtime(dft["performance (s.)"].median())), size="small",ha="left",xy=(dft["performance (s.)"].median()+7,0.0014))



    performances =  min(dft["performance (s.)"])     
    ax.annotate("Personal Best", size="small",ha="left",xy=(616,0.0103))
    if not empty:
        ax.annotate(time.strftime('%M:%S',time.gmtime(performances)), size="small",ha="left",xy=(620,0.0098))
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

    if folder is None:
        sns.plt.savefig("output2/"+str(c).zfill(3)+".png")
    elif not name is None:
        sns.plt.savefig("output2/"+name+".png")

    else:
        if not os.path.exists("output2/"+folder):
            os.makedirs("output2/"+folder)
        sns.plt.savefig("output2/"+folder+"/"+str(c).zfill(3)+".png")

    # sns.plt.title(k)
    # plt.show()  
    sns.plt.clf()
    # quit()


def CreateGraphOfStats(df,interval=30):
    i = 0
    j = interval
    length = df.count()["date"]-1
    c = 0

    data = []
    while i < length-10 and j<length:
        if j >=length-1:
            i+=1

        if j-i < interval and j < length:
            j+=1        
        elif j-i >= interval:
            j+=1
            i+=1
        else:
            i+=1



        # Make sure you are not moving over to a new season
        if df.iloc[i]["year"]!= df.iloc[j]["year"]:
            j-=1
            i+=1 
        if j-interval is i: 
            j+=interval+1
            i+=1

        c+=1

        #Get the data
        mask = (df["id"] >= i )& (df["id"] <= j)
        dft = df[mask]
        # Data, "date","year","avg","median","std","min"
        data.append([dft["date"].iloc[dft["date"].count()/2],dft["year"].iloc[0],
            (dft["date"].iloc[dft["date"].count()/2] - df["date"].iloc[0]).days,
            dft["performance (s.)"].mean(),
            dft["performance (s.)"].median(),dft["performance (s.)"].std(),dft["performance (s.)"].min()])
        # print data

        # break 
    dft  = pd.DataFrame(data,columns=["date","year","d_days","avg","median","std","min"])


    # fig = plt.figure()
    # ax = fig.axes
    # ax.errorbar(dft["d_days"],dft["median"],yerr = dft["std"],linewidth = 1,alpha=0.5 ,fmt=".")
    ax = sns.regplot(x="d_days",y="median",data=dft,order=2,label='Medians')
    ax = sns.regplot(x="d_days",y="avg",color='r',data=dft,order=2,label = 'Means')
    ax = sns.regplot(x="d_days",y="min",color='g',data=dft,order=2,label = "Mins")

    ax.legend()

    values = ax.yaxis.get_majorticklocs()
    labels2 = []
    for v in values:
        labels2.append(time.strftime('%M:%S',time.gmtime(v)))

    ax.set_yticklabels(labels2)
    ax.set_ylabel("Effort (minutes : seconds)")


    values = ax.xaxis.get_majorticklocs()
    labels2 = []
    for v in values:
        day =  datetime.timedelta(days=int(v))
        labels2.append( (df["date"].iloc[0] + day).strftime('%B\n%Y') )

    ax.set_xticklabels(labels2)
    ax.set_xlabel("Dates (month, year)")

    ax.set_title("Plot statistic (each point: n = " + str(interval) + ")" )

    plt.tight_layout()
    plt.savefig("output2/stats_plot.png")    
    plt.show()

def CreateGraphInterval(df,pos0 = None,pos1=None,c=None,folder=None):

    if pos0 is None:
        pos0 = 0
    if pos1 is None:
        pos1 = df["date"].count()-1
    if c is None:
        c = "all"

    #try to make a 1d heat map
    # fig = plt.figure(0)
    gs = matplotlib.gridspec.GridSpec(2, 1, height_ratios=[1, 5],hspace=0.05)

    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    # print ax
    # gs.tight_layout(fig)



    # This creates the first plot. We are interested in showing 
    # a cloud distribution of the points. 
    x = np.array(df["date"])
    y = np.array(df["performance (s.)"])
    ax1.plot(x,y,"o")


    start, end = ax1.get_ylim()

    labels = ax1.get_yticks().tolist()


    for i in range(len(labels)):
        if i % 2 is 1:
            labels[i] = ""
        else:
            labels[i] = time.strftime('%M:%S',time.gmtime(labels[i]))
    labels[0]=""


    # a = np.arange(start, end, len(labels)))

    ax1.set_yticklabels(labels)


    ax1.xaxis.tick_top()
    num_days = df["date"][pos1] - df["date"][pos0]
    
    ax1.add_patch(Rectangle( (df["date"][pos0],start),num_days.days,end,facecolor='gray',alpha = 0.3 ))

    # ax1.xlabel(verticalalignment="top")

    ax1.set_ylabel("performance (m:s)")


    ax1.set_title("Distribution performances, n = "+
        str(pos1-pos0),y = 1.35)



    #Second part of the plot



    timeData = []
    for r in df.iterrows():
        timeData.append(r)

    dft = df[pos0:pos1]
    
    # print timeData[i][1]["date"]
    # print s
    # print dft[45].day
    # print dft[46].day
    # quit()


    if int(dft["date"].count()) == 1:

        st = list(dft.iloc[0])
        # print st 

        st1 = copy.copy(st)
        st1[5] = st[5]+10
        dft = pd.DataFrame([st,st1],columns=["date", "date_text","year","month","day","performance (s.)","id"])




    ax  = sns.distplot(dft["performance (s.)"],hist=False,rug=True, color="b",ax=ax2)
    
    maxValue.append( sns.plt.axis()[3])
    # sns.kdeplot(dft["performance (s.)"], bw=2, label="bw: 2")

    sns.plt.axvline(dft["performance (s.)"].median(), color='#101010', linestyle='--', linewidth=1.3,alpha=0.5)
    # sns.plt.axvline(dft["performance (s.)"].mean(), color= '#101010', linestyle='-.', linewidth=1.3)
    
    d1 = str(timeData[pos0][1]["year"]) + "/" + str(timeData[pos0][1]["month"]).zfill(2) + "/" + str(timeData[pos0][1]["day"]).zfill(2)
    d2 = str(timeData[pos1][1]["year"]) + "/" + str(timeData[pos1][1]["month"]).zfill(2) + "/" + str(timeData[pos1][1]["day"]).zfill(2)

    ax.annotate(d1 + " to " + d2,ha="left",xy=(550,0.0112))
    

    #Mention that a new season started

    # if not d1[3] in d2[3]:
    #     ax.annotate("New season",size="small",xy = [307,0.0113] )
        # print "hello"
    
    ax.annotate(time.strftime('%M:%S',time.gmtime(dft["performance (s.)"].median())), size="small",ha="left",xy=(dft["performance (s.)"].median()+7,0.0014))



    performances =  min(dft["performance (s.)"])     
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

    if folder is None:
        sns.plt.savefig("output2/"+str(c).zfill(3)+".png")
    else:
        if not os.path.exists("output2/"+folder):
            os.makedirs("output2/"+folder)
        sns.plt.savefig("output2/"+folder+"/"+str(c).zfill(3)+".png")

    # sns.plt.title(k)
    # plt.show()  
    sns.plt.clf()
    # quit()


def CreateIntervalDatesAnimation(df,interval = 30,step=2):
    date_init = df["date"][0]
    date_final = list(df.iloc[-1:]["date"])[0]
    s = list(pd.date_range(start=date_init,end=date_final,freq=str(step)+"D"))

    
    
    c = 0
    i = 0 
    j = 0

    while i < len(s)-2:
        if (s[j]-s[i]).days < interval-1 and i is 0:
            j+=1
        elif(s[j]-s[i]).days >= interval-1 and j <len(s)-1:
            i+=1
            j+=1
        else:
            i+=1
        
        c+=1
        # print "index",i,j,"dates",s[i],s[j],":", (s[j]-s[i]).days
        CreateGraphIntervalDates(df,s[i],s[j],c,folder="test2")
        # return



def CreateIntervalAnimation(df,interval=30,folder = "test"):
    i = 0
    j = 1
    length = df.count()["date"]-1
    c = 0


    while i < length-10:
        if  j-i < interval and j<length:
            j+=1
        else:
            i+=1
            if j<length:
                j+=1
        
        if j is length:
            j -=1

        c+=1

        CreateGraphInterval(df,i,j,c,folder=folder)


def CreateIntervalRespectSeason(df,interval=30,folder="test"):


    i = 0
    j = 1
    length = df.count()["date"]-1
    c = 0


    while i < length-10:
        if j >=length-1:
            i+=1

        if j-i < interval and j < length:
            j+=1        
        elif j-i >= interval:
            j+=1
            i+=1
        else:
            i+=1



        # Make sure you are not moving over to a new season
        if df.iloc[i]["year"]!= df.iloc[j]["year"]:
            j-=1
            i+=1 
        if j is i: 
            j+=2
            i+=1

        c+=1
        # print i,j
        CreateGraphInterval(df,i,j,c,folder=folder)







directory = "output/"

f = open("camillien_houde_JTremblay.data")
data = []
day = None
c=0
for i in f:
    if "-" in i:
        # day = time.strptime(i[0:10].replace("-"," "),"%Y %m %d")
        day = i[0:10].replace("-","/")
        day_t = int(i[0:10].replace("-",""))
    else: 
        # performance = time.strptime(i.replace("\n",""),"%H:%M:%S")
        performance = i.replace("\n","")
        p = pd.Timestamp(performance)
        data.insert(0,[pd.Timestamp(pd.to_datetime(day)),day_t,day[0:4],day[5:7],day[8:],p.minute * 60 + p.second])
        
f.close()    

for i in range(len(data)):
    data[i].append(i)



df = pd.DataFrame(data,columns=["date", "date_text","year","month","day","performance (s.)","id"])

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






#Call the method here 
# 
# 
# 


# EXAMPLE FOR CREATING DATA FOR A YEAH
# dft = df[df["year"]=="2015"]
# pos0,pos1=list(dft.id)[0],list(dft.id)[-1]

# CreateGraphInterval(df,0,df["date"].count()-1)



# Create a animation for the whole year
# CreateIntervalAnimation(df)


# EXAMPLE WHEN PASSING DATES
dft = df[df["year"]=="2015"]
d0,d1=list(dft.id)[0],list(dft.id)[-1]
d0 =  dft["date"][d0]
d1 =  dft["date"][d1]
CreateGraphIntervalDates(df,d0,d1,folder='',name="2015")

# 
dft = df[df["year"]=="2014"]
d0,d1=list(dft.id)[0],list(dft.id)[-1]
d0 =  dft["date"][d0]
d1 =  dft["date"][d1]
CreateGraphIntervalDates(df,d0,d1,folder='',name="2014")

# 
dft = df[df["year"]=="2013"]
d0,d1=list(dft.id)[0],list(dft.id)[-1]
d0 =  dft["date"][d0]
d1 =  dft["date"][d1]
CreateGraphIntervalDates(df,d0,d1,folder='',name="2013")


d0,d1=list(df.id)[0],list(df.id)[-1]
d0 =  df["date"][d0]
d1 =  df["date"][d1]
CreateGraphIntervalDates(df,d0,d1,folder='',name="all")


# EXAMPLE CREATING ANIMATION WITH DAYS 
# LOTS OF DYING TIME
# CreateIntervalDatesAnimation(df,interval=30,step=2)

# EXAMPLE ANIMATION BUT RESPECTING YEARS
# CreateIntervalRespectSeason(df)

# EXAMPLE OF ALL THE STATS PLOTED 
# CreateGraphOfStats(df,interval=20)


# dft = df[df["year"]=="2015"]
# dft = dft.reset_index(drop=True)
# CreateIntervalAnimation(dft,folder ="2015")

# dft = df[df["year"]=="2014"]
# dft = dft.reset_index(drop=True)
# CreateIntervalAnimation(dft,folder ="2014")

# dft = df[df["year"]=="2013"]
# dft = dft.reset_index(drop=True)


# CreateIntervalRespectSeason(df,folder ="all")


quit()














