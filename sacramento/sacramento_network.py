import pandas as pd
import os
from ../s6_clipping_regions import clip
from ../s7_filter3_stronglyconnected import *

#Clipping
alllinks = pd.read_csv('/networks_dataset_Mobiliti/Nov2019/for_drive/July2021/all_links.csv')
allnodes = pd.read_csv('/networks_dataset_Mobiliti/Nov2019/for_drive/all_nodes_noferry_thrufilter.csv')
new = allnodes['geometry'].str.split(expand=True)
allnodes['LON']= new[1].str[1:]
allnodes['LAT']= new[2].str[:-1]

print("Clipping Sacramento ...")
clipboundarypath = " " #arcgis rectangular boundary generated
popdensitypath = " " #arcgis generated from GHS raster file
clip(clipboundarypath, popdensitypath, savename = 'sf', links = alllinks, nodes = allnodes)


#Strongly connected network filter
path1 = "" # files generated from above step
path2 = ""
path3 = ""
full_connected_filter(path1,path2,path3,"sf")
