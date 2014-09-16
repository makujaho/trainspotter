import sys
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader 
import matplotlib.pyplot as plt
import json

# Configuration
plt.rcParams['savefig.dpi'] = 1000

# Use equirectangular projection
ax = plt.axes(projection=ccrs.PlateCarree())

# Create the outer shape of Germany
fname = 'DEU_adm1.shp'
adm1_shapes = list(shpreader.Reader(fname).geometries())
ax.coastlines(resolution='10m')
ax.add_geometries(adm1_shapes, ccrs.PlateCarree(),
                  edgecolor='black', facecolor='gray', alpha=0.5)

# Set the image boundary to show a map section with Germany
ax.set_extent([4, 16, 47, 56], ccrs.PlateCarree())

# Read the plot data into lists
#plt.figure(figsize=(1,1))
x, y = [[],[],[],[]], [[],[],[],[]]

with open(sys.argv[1]) as f:
    for i in f:
        tmp = json.loads(i)
        if not tmp['delay'] or int(tmp['delay']) < 10:
            c = 0
        elif int(tmp['delay']) < 30:
            c = 1
        elif int(tmp['delay']) < 60:
            c = 2
        else:
            c = 3
        x[c].append(float(tmp['x'])/10**6)
        y[c].append(float(tmp['y'])/10**6)

#heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
#extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

#plt.figure(figsize=(1,1))
if len(x[0]) > 0:
    plt.plot(x[0], y[0], color='green', linewidth=0, marker='.',
             transform=ccrs.Geodetic())

if len(x[1]) > 0:
    plt.plot(x[1], y[1], color='yellow', linewidth=0, marker='.',
             transform=ccrs.Geodetic())

if len(x[2]) > 0:
    plt.plot(x[2], y[2], color='orange', linewidth=0, marker='.',
             transform=ccrs.Geodetic())

if len(x[3]) > 0:
    plt.plot(x[3], y[3], color='red', linewidth=0, marker='.',
             transform=ccrs.Geodetic())

# Set the title to the file name
plt.title(sys.argv[1].split('/')[-1])

plt.savefig(sys.argv[2],dpi=300)

#plt.clf()
#plt.imshow(heatmap, extent=extent)
#plt.show()

