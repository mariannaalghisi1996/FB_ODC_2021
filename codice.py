# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:21:15 2021

@author: maria
"""

import pandas as pd
import glob
import os
import shutil 


def gridData(csvfiles):
    # definition of the path to necessary folders and files:
    grid_path = 'C:/git/FB_ODC_2021/griglia_csv/GRIGLIA_MILANO.csv'  
    path_to_netcdf_folder = 'C:/git/FB_ODC_2021/netcdf_files'
    origin = 'C:/git/FB_ODC_2021/empty_yaml.yaml'
    # 2) Once having determined the csv to upload we can proceed with the processing of the data
    #    First we need to upload the grid (for further details on grid realization see 'grid.py')
    grid = pd.read_csv(grid_path)
    
    #    All the csv are loaded as pandas dataframe, then are joined to the grid on quadkey 
    gridded_csv = []
    #all_datetimes = []
    for i in range(len(csvfiles)):
        temp_df = pd.read_csv(csvfiles[i])
        # Not necessary columns are dropped
        temp_df = temp_df.drop(columns = ['country','lon', 'lat', 'n_baseline', 'n_difference', 'density_crisis', 'density_baseline', 'percent_change', 'clipped_z_score', 'ds'])
        # nan values are set to 0
        temp_df['n_crisis'] = temp_df['n_crisis'].replace( '\\N', 0)
        temp_df['n_crisis'] = temp_df['n_crisis'].astype(float)
        # merge on the quadkey
        temp_gridded = grid.merge(temp_df, on = 'quadkey', how = 'outer')
        temp_gridded = temp_gridded.rename(columns = {'latitude_g':'latitude', 'longitude_g':'longitude'})
        temp_gridded['n_crisis'].fillna(0, inplace=True)
        # all the datetimes are stored in a list that will be uset to name the NETCDF files
        datetime = (((csvfiles[i].split('_'))[3]).split('.'))[0]  
        #all_datetimes.append(datetime)
        temp_gridded['date_time'] = datetime
        #temp_gridded['date_time']  = pd.to_datetime(temp_gridded['date_time'] , format = "%Y-%m-%dT%H:%M:%S")
        temp_gridded = temp_gridded.set_index(['quadkey'])
        # all gridded csv are stored in gridded_csv
        gridded_csv.append(temp_gridded)
        print('ok',i,'gridded')
        temp_xarray = temp_gridded.to_xarray()
        print('ok',i,'to xarray')
        netcdf_path = path_to_netcdf_folder+'/'+datetime+'.nc'
        temp_xarray.to_netcdf(netcdf_path)
        print('ok',i,'in netcdf')
    
        # REALIZATION OF yaml DATASET
        datetime_string = datetime[0:10]+"T"+datetime[11]+datetime[12]+":"+datetime[13]+datetime[14]+":00.000Z"
        PID = list(datetime)
        PID.remove("-")
        PID.remove("-")
        PID.remove(" ")
        PID = "".join(PID)
        file1 = open(origin, "w")
        to_write = "$schema: https://schemas.opendatacube.org/dataset \n \nid: 00000000-0000-0000-0000-"+PID+"\n\nproduct:\n  name: FB_POI_MILANO\n  href: https://dataforgood.fb.com/ \n  format: NetCDF\n\ncrs: epsg:4326\n\ngeometry:\n  type: Polygon\n  coordinates: [[[ 8.995056152343800, 45.311597470877999], [8.995056152343800, 45.627484179430269], [9.549865722656120, 45.627484179430269], [9.549865722656120, 45.311597470877999], [ 8.995056152343800, 45.311597470877999]]]\n\ngrids:\n  default:\n    shape: [102,83] \n    transform: [1,0,0,0,1,0,0,0,1]\n\nlineage: {}\n\nmeasurements:\n  n_crisis:\n    layer: n_crisis\n    path: "+netcdf_path+"\n    nodata: -9999\n\nproperties:\n  odc:file_format: NetCDF\n  datetime: "+datetime_string
        file1.write(to_write)
        file1.close()
        target = "C:/git/FB_ODC_2021/cubeenv/dataset/"+PID+".yaml"
        shutil.copy(origin, target)
        #command = "datacube dataset add "+target
        #os.system(command)
    # In conclusion the names of the new peocessed csv are now written in loaded_csv.txt 
    to_write_on_txt = ",".join(csvfiles)+','
    with open("loaded_csv.txt", "a") as output:
        output.write(to_write_on_txt)
    
    return 'DONE!'

# 1) Check if there are new csv files in /Coronavirus Disease Prevention/Population Map/milan
#    to upload in OpenDataCube
fold_path = 'C:/git/FB_ODC_2021/milan'
csvfiles = []
for file in glob.glob(fold_path+"/"+"*.csv"):
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
        print('CSVs have been processed and transformed in NETCDF format, metadata dataset have been created and correctly uploaded in ODC')
        
    else:
        print('Something whent wrong :(')
else:
    print('No new csv have been found, all csv are already uploaded in ODC')