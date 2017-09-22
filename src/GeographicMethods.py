
from geopy.distance import vincenty
import numpy as np
from urllib import request
import json
from time import sleep

def get_distances(coords_x, coords_y):
    '''
    Takes two lists of lat / long coordinates (as tuple pairs).
    Returns a matrix of distances (in miles) between all pairs of coordinates from
    coords_x and coords_y.
    Rows of the matrix correspond to entries in coords_x, and columns correspond to
    entries in coords_y.
    '''
    distances = np.zeros((len(coords_x), len(coords_y)))
    for idx_x, coord_x in enumerate(coords_x):
        for idx_y, coord_y in enumerate(coords_y):
            distances[idx_x, idx_y] = vincenty(coord_x, coord_y).miles
    return distances

def count_within_distance(coords_ref, coords, radius):
    '''
    Takes two lists of lat / long coordinates (as tuple pairs).
    Returns a vector with an entry corresponding to each coordinate in coords_ref.
    Entries count the number of coordinates in coords within the given radius 
    (in miles) of the coordinate in coords_ref corresponding to the entry.
    '''
    distances = get_distances(coords_ref, coords)
    return np.sum(distances <= radius, axis = 1)

def get_altitudes(coords, delay = 0.2):
    '''
    Uses the Google Maps API to get the elevation (in meters) of each lat / long
    coordinate supplied in the list coords.
    A delay (in seconds) occurs between queries; otherwise, Google will get upset.
    Code adapted from StackOverflow:
    https://stackoverflow.com/questions/11504444/raster-how-to-get-elevation-at-lat-long-using-python
    '''
    elevations = []
    for coord in coords:
        ELEVATION_BASE_URL = 'http://maps.googleapis.com/maps/api/elevation/json?'
        URL_PARAMS = "locations=%s,%s&sensor=%s" % (coord[0], coord[1], "false")
        url = ELEVATION_BASE_URL + URL_PARAMS
        with request.urlopen(url) as f:
            sleep(0.5)
            response = json.loads(f.read().decode())    
            status = response['status']
            elevations.append(response["results"][0]['elevation'])
    return elevations







