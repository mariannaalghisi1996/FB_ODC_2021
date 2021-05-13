# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 12:50:27 2021

@author: maria
"""

import pandas as pd
from shapely.geometry import Point
import numpy as np
from sklearn.neighbors import BallTree

def get_nearest(src_points, candidates, k_neighbors=1):
    """Find nearest neighbors for all source points from a set of candidate points"""

    # Create tree from the candidate points
    tree = BallTree(candidates, leaf_size=15, metric='haversine')

    # Find closest points and distances
    distances, indices = tree.query(src_points, k=k_neighbors)

    # Transpose to get distances and indices into arrays
    distances = distances.transpose()
    indices = indices.transpose()

    # Get closest indices and distances (i.e. array at index 0)
    # note: for the second closest points, you would take index 1, etc.
    closest = indices[0]
    closest_dist = distances[0]

    # Return indices and distances
    return (closest, closest_dist)


def nearest_neighbor(left_gdf, right_gdf, return_dist=False):
    """
    For each point in left_gdf, find closest point in right GeoDataFrame and return them.

    NOTICE: Assumes that the input Points are in WGS84 projection (lat/lon).
    """

    left_geom_col = left_gdf.geometry.name
    right_geom_col = right_gdf.geometry.name

    # Ensure that index in right gdf is formed of sequential numbers
    right = right_gdf.copy().reset_index(drop=True)

    # Parse coordinates from points and insert them into a numpy array as RADIANS
    left_radians = np.array(left_gdf[left_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())
    right_radians = np.array(right[right_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())

    # Find the nearest points
    # -----------------------
    # closest ==> index in right_gdf that corresponds to the closest point
    # dist ==> distance between the nearest neighbors (in meters)

    closest, dist = get_nearest(src_points=left_radians, candidates=right_radians)

    # Return points from right GeoDataFrame that are closest to points in left GeoDataFrame
    closest_points = right.loc[closest]

    # Ensure that the index corresponds the one in left_gdf
    closest_points = closest_points.reset_index(drop=True)

    # Add distance if requested
    if return_dist:
        # Convert to meters from radians
        earth_radius = 6371000  # meters
        closest_points['distance'] = dist * earth_radius

    return closest_points



csv_file = pd.read_csv('C:/Users/maria/OneDrive - Politecnico di Milano/Desktop/GeoinfoProject/Prova/provadati3.csv')
lon_min = min(csv_file['lon'])
lon_max = max(csv_file['lon'])
lat_min = min(csv_file['lat'])
lat_max = max(csv_file['lat'])

#GRID

grid = pd.DataFrame(columns = ['id_grid','latitude_grid', 'longitude_grid', 'geometry'])
delta_lat = (lat_max - lat_min)/82
delta_lon = (lon_max - lon_min)/101
i = 0

for lon in np.arange(lon_min, lon_max+delta_lon, delta_lon):
    for lat in np.arange(lat_min, lat_max + delta_lat, delta_lat):
        p = Point(lon, lat)
        row = pd.DataFrame([[i, lat, lon, p]], columns = ['id_grid','latitude_grid', 'longitude_grid', 'geometry'])
        grid = grid.append(row)
        i = i + 1


csv_file['geometry'] = csv_file.apply(lambda _: '', axis=1)

for i in range(len(csv_file)):
    csv_file['geometry'][i] = Point(csv_file['lon'][i], csv_file['lat'][i])

csv_file['id_csv'] = (csv_file.index).astype(int)

temp_nn = nearest_neighbor(csv_file, grid, return_dist = False)
temp_nn['id_grid'] = temp_nn['id_grid'].astype(int)

temp_nn['id_to_add'] = (temp_nn.index).astype(int)

nn_merge = temp_nn.merge(csv_file, left_on = 'id_to_add', right_on = 'id_csv')

nn_merge_2 = nn_merge[['id_grid','longitude_grid', 'latitude_grid', 'geometry_x', 'quadkey']]

nn_merge_2.to_csv('C:/Users/maria/OneDrive - Politecnico di Milano/Desktop/GeoinfoProject/Controllare/griglia_sesto_tent.csv')

grid.to_csv('C:/Users/maria/OneDrive - Politecnico di Milano/Desktop/GeoinfoProject/Controllare/griglia_per_cotrollare.csv')
