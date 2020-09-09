# overlay-raster
Read a raster data file with rasterio and overlay it on folium with appropriate coloring.

# TODO
* Simplify the code -- all those functions are not necessary to show how it works
* Add projection function and check if data has the correct CRS before overlaying it on the map
* Better handling of colormaps: get the color list from branca using cmbranca.colors and then create a matplotlib LinearSegmentedColormap using from_list()
* Check consistency of colormaps
