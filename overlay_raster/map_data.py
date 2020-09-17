"""Display raster data on a map."""

import folium
import branca
import matplotlib.pyplot as plt
from overlay_raster import input, preproc


def raster_overlay(in_path, out_path, data_name, colormap="OrRd", zoom=3, opacity=0.9):
    """Overlay raster data on folium map.

    IMPORTANT: input data should already be in EPSG:4326 crs.

    Args:
        in_path (str): path of the input raster file
        out_path (str): path where the HTML map will be stored
        data_name (str): the label that will be displayed under the colorbar
        colormap (str, optional): name of the colormap. It must be an existing colormap
            both in
            * matplotlib, check https://matplotlib.org/tutorials/colors/colormaps.html
            * branca, as a 9-colors-list. It means that if the colormap's name in
            matplotlib is X, you should also be able to find X_09 within branca methods.
            You can check it by tabbing branca.colormap.linear.X_09 in python.
            Defaults to "OrRd".
        zoom (int, optional): how far the map is initially zoomed in. Defaults to 3.
        opacity (float, optional): raster data opacity on the map. Defaults to 0.9.
    """
    # Read and preprocess data
    data, coord_extent = input.read_raster(in_path)
    data_extent = input.data_extent(data)
    cmap = plt.get_cmap(colormap)
    data_color = preproc.color_data(data, cmap)

    # Overlay data on map
    lat, lon = coord_extent
    m = folium.Map(location=[lat.mean(), lon.mean()], zoom_start=zoom)
    m.add_child(
        folium.raster_layers.ImageOverlay(
            data_color,
            bounds=[[lat.min(), lon.min()], [lat.max(), lon.max()]],
            mercator_project=True,
            opacity=opacity,
        )
    )

    # Add colorbar
    cmbranca = getattr(branca.colormap.linear, colormap + '_09').\
        scale(vmin=data_extent[0], vmax=data_extent[1])
    cmbranca.caption = data_name
    cmbranca.add_to(m)

    m.save(out_path)
