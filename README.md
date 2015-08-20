# Strava

The main goal of this project is to understand better a cyclist performances on a given Strava segment. The first produced figure is a cloud of points, *e.g.*, 
![fig1](https://github.com/TontonTremblay/Strava/blob/master/example_results/Cloud_camillien_houde_JTremblay.png)
The figure shows on the x-axis a date and on the y-axis the time performance. The lower the point is, the better your performance is. In my case you see that overall my performances are getting better. 
An other way to look at this particular data is through the usage of a plot distribution, *e.g.*
![fig1](https://github.com/TontonTremblay/Strava/blob/master/example_results/Dist_camillien_houde_JTremblay.png)
On the x-axis is located the different performances time for that Strava segment. On the y-axis we find the percentage of the performances for that time. I have added the mean and median as vertical lines as well as the normal fit. This allows you to get a better sense of your performances on a particular segment. In my case we can see that I in general I am around 7 min. for that segment. The performances with 9min. and more are done with an other friend. 

##How to use
You will need some python packages that can be install with pip, 
```
pip install matplotlib
pip install stravalib
```
In order to gain access to your data you will have to register your app in Strava, moreover over you will have to create a .token with the key to client access, please refer to this [link](https://github.com/hozn/stravalib) on how to do that using stavalib. 
Once you have a athlete token saved in a file, you can downlaod your performances using `ReadDataSegment.py`, *e.g.*
```
python ReadDataSegment.py jtremblay.token "camillien houde"
```
ReadDataSegment.py connects to Strava and downlaod any performances you did on that particular segment. This might take a while since Strava limits the polling per second an third app can do. This will save a file `.data`, *e.g.* `camillien_houde_JTremblay.data`. 
In order to produce the presented graph you simply use the `plotDistribution.py` and pass the data as reference, for example,
```
python plotDistribution.py camillien_houde_JTremblay.data
```
It will then save two pdf files with your graphs.
