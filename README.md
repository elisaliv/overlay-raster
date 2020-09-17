# overlay-raster

Read a raster data file with rasterio and overlay it on folium with appropriate
coloring.

The core function to this end is `raster_overlay` inside overlay_raster/map_data.py.

## TODO

* Add projection function and check if data has the correct CRS before overlaying it on
  the map
* Add option to handle raster files with more bands
* Check if colormap exists
