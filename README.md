# FB_ODC_2021

This project aims at developing an Open Data Cube instance to manage Facebook Data for Good. The work focuses on the analysis of dataset describing the population density of the city of Milan, offering a data processing method that is sufficiently generic to be extended to other types of datasets.
The work is divided into two jupyter notebooks, the content is discussed below.

Requirements:
- ODC Python environment
   
  (installed through Anaconda --> https://datacube-core.readthedocs.io/en/latest/ops/install.html)
  
- PostGres database setup

  (we used pgAdmin UI, other references --> https://datacube-core.readthedocs.io/en/latest/ops/db_setup.html)
  More details about Database setup and initialization are given in report, chaprter 3.2.
  
- Required python packages: datacube, jupyter, pandas, geopandas, glob, os, shutil, xarray, matplotlib, numpy, ipywidgets, contextily, folium, branca

Content of the folder:
- griglia_csv: folder that contains the csv of the grid created from the Facebook Data for Good's csv, required for the gridding of the data. 
  Full explanation of grid realization is contained in the notebook.
  In addition the folder contains some csvs and josn files used for Daa Analysis
- python codes: folder that contains the python scripts (.py) used in the realization process of the notebook.
- cubeenv: folder that contains the notebook and the material required by ODC (product and datasets metadata).
- netcdf_files: folder that contains the netcdf files produced from the gridding process, file format required by datacube in order to retrieve the measurements.
- markdown: folder that contains screenshots used in the notebook to show the relevant results.

Processes and routines contained in jupyter notebook '1_griding_upload.ipynb:
1) Grid realization

   Process used for the realization of the grid that will be used for the gridding of the facebook data. 
   An example csv is loaded from the reference folder for the creation of the grid, starting from it we define grid's boundaries. The grid is realized as a pandas DataFrame.
   With a loop we insert in the dataframe all the points (latitude, longitude) of the grid.
   Each point of the grid is associated to a specific quadkey (retrieved from the original csv) by implementing nearest neighbor algorithm.
   IMPORTANT: since in the raw data there are some missing points, missing quadkeys have been added manually through QGIS.
   See Chapter 2 of the report.

2) CSV gridding, transformation in NetCDF, metadata realization and upload on ODC

   A simple routine is implemented in order to check if there are new csv from Facebook in 'milan' folder. If new csvs are detected, the function gridData is called.
   gridData takes as input the list of the new csvs and process them: all the csv are loaded as pandas dataframe, then are joined to the grid on quadkey.
   The resulting grid will contain the following columns: time, latitude, longitude, n_crisis (where n_crisis contains the information about density population).
   The grid is then converted in xarray and then saved as netcdf file in 'netcdf_folder'.
   The process continues with the realization of the metadata yaml file that describes the dataset that will be uploaded on ODC.
   Once the dataset is ready and saved in 'cubeenv/dataset' folder, with a system command (datacube dataset add newfile.yaml), the dataset is loaded in ODC.
   The process finishes with the update of the text file than contains the list of the csv already present in the database.
   See chapter 3.1 of the report
   
3) General information about ODC

   Shows some general command used to inspect the content of the database (information on products).

Processes and routine contained in jupyter notebook '2_data_analysis.ipynb:
   
1) Loading data

   Focus on the usage of the load function (DataCube.load --> https://datacube-core.readthedocs.io/en/latest/dev/api/generate/datacube.Datacube.load.html )
   Some widgets are used in order to allow the user to specify his preferences on the time interval to analyze.
   
2) Data Analysis

   Show an example on the possible computation and analysis that can be performed on the data:
   - Plot of mean/variance/median over time interval
   - Temporal series for a selected point (longitude, latitude)
   - Production of a grid where each point stores the value of mean/variance/median of the point over time range
     Plot of the raw data, html map creation with folium library
   - Focus on population distribution of Milano's districts, plot on a basemap
