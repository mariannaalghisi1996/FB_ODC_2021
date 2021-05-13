# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:21:15 2021

@author: maria
"""

import pandas as pd
import numpy as np
import glob
import os
import xarray
import netCDF4

def gridData(csvfiles):
    # 2) Once having determined the csv to upload we can proceed with the processing of the data
    #    First we need to upload the grid (for further details on grid realization see 'grid.py')
    grid = pd.read_csv(r'Prova griglia/GRIGLIA_MILANO.csv')
    
    #    All the csv are loaded as pandas dataframe, then are joined to the grid on quadkey 
    gridded_csv = []
    all_datetimes = []
    for i in range(len(csvfiles)):
        temp_df = pd.read_csv(csvfiles[i])
        # Not necessary columns are dropped
        temp_df = temp_df.drop(columns = ['lon', 'lat', 'n_baseline', 'n_difference', 'density_crisis', 'density_baseline', 'percent_change', 'clipped_z_score', 'ds'])
        # nan values are set to 0
        temp_df['n_crisis'] = temp_df['n_crisis'].replace( '\\N', 0)
        temp_df['n_crisis'] = temp_df['n_crisis'].astype(float)
        # merge on the quadkey
        temp_gridded = grid.merge(temp_df, on = 'quadkey', how = 'outer')
        temp_gridded['n_crisis'].fillna(0, inplace=True)
        temp_gridded['country'].fillna('IT', inplace=True)
        # all the datetimes are stored in a list that will be uset to name the NETCDF files
        datetime = (((csvfiles[i].split('_'))[1]).split('.'))[0]
        all_datetimes.append(datetime)
        temp_gridded['date_time'].fillna(datetime)
        # all gridded csv are stored in gridded_csv
        gridded_csv.append(temp_gridded)
    
    # All the csv are now transformed in xarrays and then in NETCDF files contained in 'netcdf_files' folder
    path_to_netcdf_folder = '/netcdf_files'
    
    all_xarrays = []
    for j in range(len(csvfiles)):
        temp_xarray = gridded_csv[j].to_xarray()
        all_xarrays.append(temp_xarray)
        temp_NETCDF = temp_xarray.to_netcdf(path_to_netcdf_folder+'/'+all_datetimes[j]+'.nc')
        yaml_text = open("empty_txt.yaml")
        yaml_text.write("""$schema: https://schemas.opendatacube.org/dataset

        id: 000000000 0000 2020 04050000

        product:
        name: FACEBOOKDATAFORGOOD_MILANPOPULATION
        href: https://dataforgood.fb.com/
        format: NetCDF

        crs: epsg:4326

        geometry:
        type: Polygon
        coordinates: [[[ 8.995056152343800, 45.311597470877999], [8.995056152343800, 45.627484179430269], [9.549865722656120, 45.627484179430269], [9.549865722656120, 45.311597470877999], [ 8.995056152343800, 45.311597470877999]]]

        grids:
        default:
        shape: numero di punti in latitudine e longitudine, in rispetto a un intervallo tra un valore e l'altro
        transform: [1,0,0,0,1,0,0,0,1]

        lineage: {}

        measurements:
        valore:
        layer: n-crisis
        path: """+ path_to_netcdf_folder +"""
        nodata: -9999

        properties:
        odc:file_format: NetCDF
        datetime: """+ datetime +"""Z
        """)
        yaml_text.close()
        #os.system("""Path to Datacube; datacube dataset add YAML FILE""")
    
    # In conclusion the names of the new peocessed csv are now written in loaded_csv.txt 
    to_write_on_txt = ",".join(csvfiles)+','
    with open("loaded_csv.txt", "a") as output:
        output.write(to_write_on_txt)
    
    return 'DONE!'


# 1) Check if there are new csv files in /Coronavirus Disease Prevention/Population Map/milan
#    to upload in OpenDataCube
fold_path = 'C:/Users/marti/OneDrive - Politecnico di Milano/Coronavirus Disease Prevention/Population Map/milan'
csvfiles = []
for file in glob.glob(fold_path+'/'+"*.csv"):
    # We only consider not-empy files
    if os.stat(file).st_size != 0:
        csvfiles.append(file)

# 'loadedCSV.txt' contains all the names of the already loaded files
# already_loaded is a list containing these files names
with open("loaded_csv.txt", "r") as txt:
    already_loaded = (txt.read()).split(',')

# in order to check if there are new csv i use a loop that removes from csvfiles list 
# the names of the already loaded csv
for name in already_loaded:
    if name in csvfiles:
        csvfiles.remove(name)  


if len(csvfiles) != 0:
    print(len(csvfiles), 'new CSVs have been found')
    print('Processing of CSVs is started...')
    ret = gridData(csvfiles)
    if ret == 'DONE!':
        print('CSVs have been processed and transformed in NETCDF format')
        
    else:
        print('Something whent wrong :(')
else:
    print('No new csv have been found, all csv are already uploaded in ODC')

def gridData(csvfiles):
    # 2) Once having determined the csv to upload we can proceed with the processing of the data
    #    First we need to upload the grid (for further details on grid realization see 'grid.py')
    grid = pd.read_csv(r'Prova griglia/GRIGLIA_MILANO.csv')
    
    #    All the csv are loaded as pandas dataframe, then are joined to the grid on quadkey 
    gridded_csv = []
    all_datetimes = []
    for i in range(len(csvfiles)):
        temp_df = pd.read_csv(csvfiles[i])
        # Not necessary columns are dropped
        temp_df = temp_df.drop(columns = ['lon', 'lat', 'n_baseline', 'n_difference', 'density_crisis', 'density_baseline', 'percent_change', 'clipped_z_score', 'ds'])
        # nan values are set to 0
        temp_df['n_crisis'] = temp_df['n_crisis'].replace( '\\N', 0)
        temp_df['n_crisis'] = temp_df['n_crisis'].astype(float)
        # merge on the quadkey
        temp_gridded = grid.merge(temp_df, on = 'quadkey', how = 'outer')
        temp_gridded['n_crisis'].fillna(0, inplace=True)
        temp_gridded['country'].fillna('IT', inplace=True)
        # all the datetimes are stored in a list that will be uset to name the NETCDF files
        datetime = (((csvfiles[i].split('_'))[1]).split('.'))[0]
        all_datetimes.append(datetime)
        temp_gridded['date_time'].fillna(datetime)
        # all gridded csv are stored in gridded_csv
        gridded_csv.append(temp_gridded)
    
    # All the csv are now transformed in xarrays and then in NETCDF files contained in 'netcdf_files' folder
    path_to_netcdf_folder = 'C:/Users/marti/OneDrive - Politecnico di Milano/FBproject/project/netcdf_files/'
    
    all_xarrays = []
    for j in range(len(csvfiles)):
        temp_xarray = gridded_csv[j].to_xarray()
        all_xarrays.append(temp_xarray)
        temp_NETCDF = temp_xarray.to_netcdf(path_to_netcdf_folder+'/'+all_datetimes[j]+'.nc')
    
    # In conclusion the names of the new peocessed csv are now written in loaded_csv.txt 
    to_write_on_txt = ",".join(csvfiles)+','
    with open("loaded_csv.txt", "a") as output:
        output.write(to_write_on_txt)
    
    return 'DONE!'