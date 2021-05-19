# -*- coding: utf-8 -*-
"""
Created on Wed May 19 16:12:28 2021

@author: maria
"""

import glob
import os
import shutil
from datetime import datetime

fold_path = 'C:/git/FB_ODC_2021/netcdf_files/'
netcdf_files = []
PID_values = []
datetimes = []
for file in glob.glob(fold_path+"/"+"*.nc"):
    dt = file[37:47]
    dt = list(dt)
    dt.remove("-")
    dt.remove(" ")
    dt = "".join(dt)
    # We only consider not-empy files
    if os.stat(file).st_size != 0:
        netcdf_files.append(file)
        datetimes.append(dt)

origin = 'C:/git/FB_ODC_2021/empty_yaml.yaml'

for i in range(len(netcdf_files)):
    PID = datetimes[0]
    netcdf_path = netcdf_files[0]
    file1 = open(origin, "w")
    to_write = """$schema: https://schemas.opendatacube.org/dataset

id: 00000000-0000-0000-0000-"
"""+ PID +"""

product:
  name: FB_POI_MILANO
  href: https://dataforgood.fb.com/
  format: NetCDF

crs: epsg:4326

geometry:
  type: Polygon
  coordinates: [[[ 8.995056152343800, 45.311597470877999], [8.995056152343800, 45.627484179430269], [9.549865722656120, 45.627484179430269], [9.549865722656120, 45.311597470877999], [ 8.995056152343800, 45.311597470877999]]] 

grids:
  default:
    shape: [102,83]
    transform: [1,0,0,0,1,0,0,0,1]

lineage: {}

measurements:
  n_crisis:
    layer: n_crisis
    path: """+netcdf_path+"""
    nodata: -9999

properties:
  odc:file_format: NetCDF
  datetime: 2021-01-15T13:00:00.000
  """"
)        

import shutil

origin = 'C:/git/FB_ODC_2021/empty_yaml.yaml'
     
file1 = open(origin, "w")

toFile = "Write what you want into the field"

target = 'C:/git/FB_ODC_2021/products/test_yaml.yaml'
file1.write(toFile)
file1.close()
shutil.copy(origin, target)    
