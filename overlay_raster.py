"""Read a raster data file with rasterio and overlay it on folium with appropriate
coloring.
I set the OrRd colormap as default in both functions (display on map or just plot
data), please change it depending on what you like and need.
Just make sure to use a matplotlib *linear* colormap and the corresponding branca
*_09 colormap.

IMPORTANT: this code works fine for input data with EPSG:4326 CRS (coordinate reference
system). The data should be projected on this CRS before displaying it on a map.

elisaliv, 9-Sep-2020
"""

import numpy as np
import rasterio as rio
import folium
import branca
import matplotlib.pyplot as plt
from matplotlib import cm, colors

dirpath = "<path>"
filename = "<name>.tif"
filepath = dirpath + filename


def read_raster(filepath):
    # Read data from geo-raster file, e.g. TIF
    src = rio.open(filepath)
    data = src.read(1)
    lon = np.array([src.bounds.left, src.bounds.right])
    lat = np.array([src.bounds.bottom, src.bounds.top])
    coord_extent = [lat, lon]
    # Also returns coordinate extent
    src.close()
    return data, coord_extent


data_name, coords = read_raster(filepath)


def data_extent(data):
    # Calculate data extent (later used to normalize plot colors)
    numbers = data[~np.isnan(data)]
    data_lims = [numbers.min(), numbers.max()]
    return data_lims


minmax = data_extent(data_name)


def color_data(data, data_extent, cmap_obj=cm.OrRd):
    # Prepare colored and normalized data to be overlayed on map
    norm = colors.Normalize(vmin=data_extent[0], vmax=data_extent[1])
    data_color = cmap_obj(norm(data))
    return data_color


data_name_color = color_data(data_name, minmax)


def folium_overlay(data_color, coord_extent, data_extent, map_path):
    # Overlay raster data on folium map
    # folium options should be changed inside this function (e.g. opacity)
    lat, lon = coord_extent
    m = folium.Map(location=[lat.mean(), lon.mean()], zoom_start=3)
    m.add_child(
        folium.raster_layers.ImageOverlay(
            data_color,
            bounds=[[lat.min(), lon.min()], [lat.max(), lon.max()]],
            mercator_project=True,
            opacity=0.9,
        )
    )
    # Add colorbar using a LinearColormap object (must be created with branca)
    cmbranca = branca.colormap.linear.OrRd_09.scale(vmin=data_extent[0],
                                                    vmax=data_extent[1])
    cmbranca.caption = '<data name [unit]>'
    cmbranca.add_to(m)
    m.save(map_path)


folium_overlay(data_name_color, coords, "map.html")
# Last arg is where the map will be stored locally


def plot_data(data, coord_extent, data_extent, cmap_str="OrRd"):
    # Simply plot the data adjusting coordinate labels and normalizing colormap
    lat, lon = coord_extent
    plt.imshow(data, cmap=cmap_str, extent=(lon.min(), lon.max(), lat.min(), lat.max()))
    plt.clim(data_extent[0], data_extent[1])
    plt.colorbar()

    plt.show()


plot_data(data_name, coords, minmax)
# You don't need to input already colored data for this function
