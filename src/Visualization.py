
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

BASEMAP_SHAPEFILE = './data/zoning/geo_export_9b2ff14a-9707-4815-b62d-473c20e22332'

# Frame settings
LOWER_CORNER = (37.77, -122.43)
UPPER_CORNER = (37.81, -122.37)
ORIGIN = (37.779250, -122.419305) # Location of SF city hall

# Other Settings
FIG_SIZE = (8, 6)
DPI = 80
WATER_COLOR = '#A3CCFF'

# Create basemap
MAP = Basemap(
    llcrnrlon = LOWER_CORNER[1],
    llcrnrlat = LOWER_CORNER[0],
    urcrnrlon = UPPER_CORNER[1],
    urcrnrlat = UPPER_CORNER[0],
    projection = 'tmerc', 
    resolution = 'f',
    lat_0 = ORIGIN[0], lon_0 = ORIGIN[1])

def draw_network_on_basemap(longs, lats, weights):

    plt.figure(figsize = FIG_SIZE, dpi = DPI)

    # Plot geography
    MAP.drawmapboundary(fill_color = WATER_COLOR)
    MAP.fillcontinents(lake_color = WATER_COLOR)
    MAP.drawcoastlines()

    # Plot zones
    MAP.readshapefile(BASEMAP_SHAPEFILE, 'zoning')

    # Plot stations
    MAP.scatter(longs, lats, latlon=True, marker='o', c='C1', s=40, zorder=10)

    # Plot edges
    n = len(longs)
    N = np.max(weights)
    for i in range(n):
        for j in range(n):        
            xx = [longs[i], longs[j]]
            yy = [lats[i], lats[j]]
            MAP.plot(xx, yy, '-', linewidth=2, \
                alpha=weights[i,j] / N, color='C0', zorder=20, latlon=True)

    return None   

def draw_source_dest_heatmap(x, labels):

    plt.figure(figsize = FIG_SIZE, dpi = DPI)
    plt.imshow(x, interpolation = 'nearest', cmap = 'hot')
    plt.xticks(range(len(labels)), labels, rotation = 'vertical')
    plt.yticks(range(len(labels)), labels)
    plt.colorbar()

    return None
