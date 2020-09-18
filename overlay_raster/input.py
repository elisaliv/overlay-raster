"""Read an input raster file and its extent."""

import numpy as np
import rasterio as rio


def read_raster(filepath):
    """Read data from geo-raster file, e.g. geoTIF.

    Raster files can have more layers (bands). This function assumes the TIF file only
    has one band.
    It is also assumed that input data is already in EPSG:4326 crs.

    Args:
        filepath (str): path of the file

    Returns:
        np.array, list: array containing the data,
            list with coordinate extent of data in the form
            [np.array([bottom_latitude, top_latitude]),
             np.array(left_longitude, right_longitude)]
    """
    src = rio.open(filepath)
    data = src.read(1)  # read first band
    lon = np.array([src.bounds.left, src.bounds.right])
    lat = np.array([src.bounds.bottom, src.bounds.top])
    coord_extent = [lat, lon]
    src.close()
    return data, coord_extent


def data_extent(data):
    """Calculate data extent of numpy array.

    Args:
        data (numpy.ndarray): data to be examined

    Returns:
        list: list in the form [data_min, data_max]
    """
    numbers = data[~np.isnan(data)]
    data_lims = [numbers.min(), numbers.max()]
    return data_lims
