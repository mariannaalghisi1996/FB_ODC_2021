import glob
import os

fold_path = 'C:/git/FB_ODC_2021/cubeenv/dataset'
meta_files = []
for file in glob.glob(fold_path+"/"+"*.yaml"):
    if os.stat(file).st_size != 0:
        meta_files.append(file)

for path in meta_files:
	command = 'datacube dataset add ' + path
	os.system(command)