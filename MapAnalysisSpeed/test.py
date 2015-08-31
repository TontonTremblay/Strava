from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap(projection='tmerc',
	lat_0 = 30., lon_0 = -27.,
	llcrnrx=500000.,llcrnry=500000.,urcrnrx=2700000.,urcrnry=2700000.)


map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()
 
plt.show()