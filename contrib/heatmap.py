import sys
from mpl_toolkits.basemap import Basemap, cm
from numpy import array
import matplotlib.pyplot as plt
import matplotlib.colors as cl
import numpy as np
import json

# Configuration
plt.rcParams['savefig.dpi'] = 300

# set up a basemap with stereographic projection aiming
# roughly at germany
map = Basemap(projection='stere', lat_0=0, lon_0=0, resolution='i',
              llcrnrlon=4, llcrnrlat=47,urcrnrlon=17,urcrnrlat=56)

# nice background graphics
map.shadedrelief()

# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.5)
map.drawcountries(linewidth=0.5)

# Read the plot data into lists
sizes, data, x, y = [], [],[],[]
 
# min and max values somewhere outside the map
# needed to generate a steady cbar
x.append(4)
y.append(46)
sizes.append(0)
data.append(0)
x.append(4)
y.append(46)
sizes.append(0)
data.append(180)

with open(sys.argv[1]) as f:
    for i in f:
        tmp = json.loads(i)
        if not tmp['delay']: tmp['delay'] = 0
        data.append(int(tmp['delay']))
        sizes.append(5)
        x.append(float(tmp['x'])/10**6)
        y.append(float(tmp['y'])/10**6)

# sanitize that data!
xo = x[:]
yo = y[:]
x, y = array(x), array(y)
x1, y1 = map(x, y)
x = np.compress(np.logical_or(x1 < 1.e20,y1 < 1.e20), x1)
y = np.compress(np.logical_or(x1 < 1.e20,y1 < 1.e20), y1)

# plot that data as heat map
map.hexbin(x, y, C=data, gridsize=50, cmap=plt.cm.jet, alpha=0.25,
           norm=cl.LogNorm())

# plot that data as scatter map
cs = map.scatter(xo, yo, c=data, s=sizes, cmap=plt.cm.jet, linewidth=0.3, 
                 latlon=True, norm=cl.LogNorm())
cbar = map.colorbar(cs,location='bottom',pad="5%",
                    ticks=[1,5,10,30,60,120], format='%.0f')
cbar.set_label('minutes delay')

# Set the title to the file name
plt.title(sys.argv[1].split('/')[-1])

# save plot as file
plt.savefig(sys.argv[2], bbox_inches='tight')