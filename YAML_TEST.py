# -*- coding: utf-8 -*-
"""
Created on Wed May 19 16:12:28 2021

@author: maria
"""

import glob
import os
import shutil

fold_path = 'C:/git/FB_ODC_2021/netcdf_files/'
netcdf_files = []
datetimes_compact = []
datetimes = []
for file in glob.glob(fold_path+"/"+"*.nc"):
    dt = ((file.split("\\")[1]).split("."))[0]
    datetime = dt[0:10]+"T"+dt[11]+dt[12]+":"+dt[13]+dt[14]+":00.000Z"
    dt = list(dt)
    dt.remove("-")
    dt.remove("-")
    dt.remove(" ")
    dt = "".join(dt)
    # We only consider not-empy files
    if os.stat(file).st_size != 0:
        netcdf_files.append(file)
        datetimes_compact.append(dt)
        datetimes.append(datetime)

origin = 'C:/git/FB_ODC_2021/empty_yaml.yaml'

for i in range(len(netcdf_files)):
    PID = datetimes_compact[i]
    netcdf_path = netcdf_files[i]
    datetime = datetimes[i]
    file1 = open(origin, "w")
    to_write = "$schema: https://schemas.opendatacube.org/dataset \n \nid: 00000000-0000-0000-0000-"+PID+"\n\nproduct:\n  name: FB_POI_MILANO\n  href: https://dataforgood.fb.com/ \n  format: NetCDF\n\ncrs: epsg:4326\n\ngeometry:\n  type: Polygon\n  coordinates: [[[ 8.995056152343800, 45.311597470877999], [8.995056152343800, 45.627484179430269], [9.549865722656120, 45.627484179430269], [9.549865722656120, 45.311597470877999], [ 8.995056152343800, 45.311597470877999]]]\n\ngrids:\n  default:\n    shape: [102,83] \n    transform: [1,0,0,0,1,0,0,0,1]\n\nlineage: {}\n\nmeasurements:\n  n_crisis:\n    layer: n_crisis\n    path: "+netcdf_path+"\n    nodata: -9999\n\nproperties:\n  odc:file_format: NetCDF\n  datetime: "+datetime
    file1.write(to_write)
    file1.close()
    target = "C:/git/FB_ODC_2021/cubeenv/dataset/"+PID+".yaml"
    shutil.copy(origin, target)
    print(i, "yaml dataset succesfully created")
    command = "datacube dataset add "+target
    os.system(command)
    print(i, "uploaded")
