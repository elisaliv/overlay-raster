"""Prepare the data for visualization."""

from matplotlib import colors, cm
from overlay_raster import input


def color_data(data, cmap_obj=cm.OrRd):
    """Prepare colored and normalized data to be overlayed on map.

    Args:
        data (np.array or similar): input data to be colored
        data_extent (list or similar): list in the form [data_min, data_max]
        cmap_obj (matplotlib.colors.ListedColormap): colormap object.
            Defaults to cm.OrRd.

    Returns:
        np.array: data filtered through colormap and normalized, ready to be displayed
            on a map
    """
    data_extent = input.data_extent(data)
    norm = colors.Normalize(vmin=data_extent[0], vmax=data_extent[1])
    data_color = cmap_obj(norm(data))
    return data_color
