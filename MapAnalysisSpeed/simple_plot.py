import pandas as pd 
import matplotlib.pyplot as plt

from mpl_toolkits.basemap  import Basemap

import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import string
import matplotlib.cm as cm
import matplotlib.pyplot as plt

df = pd.DataFrame.from_csv("data.csv")

 

print 
x = df['longitude']
y = df['latitude']



m = Basemap(llcrnrlon = x.min(),urcrnrlon = x.max(),llcrnrlat=y.min(),urcrnrlat=y.max())



x1,y1=m(x,y)
m.drawmapboundary(fill_color='white') # fill to edge
m.scatter(x,y,s=1,marker="o",color = 'blue',alpha=1.0)


plt.show()