import pandas as pd
import numpy as np
import geopandas as gpd

#Tasks
#1. Clip SF Bay Area
#2. Clip LA SCAG Region

all_nodes_noferry = pd.read_csv("\Nov2019\for_drive\all_nodes_noferry.csv")
all_links_noferry = pd.read_csv("\Nov2019\for_drive\all_links_noferry.csv")

# 1. SF Bay Area
#Arcgis clip based on Rectangular bounding box
sf_clip_geom = gpd.read_file("..\Nov2019\midstages\clip\SF_Clip.shp")
a = sf_clip_geom['LINK_ID'].to_list()
sf_links_noferry = all_links_noferry[all_links_noferry["LINK_ID"].isin(a)]
sf_links_noferry.to_csv("\networks_dataset_Mobiliti\Nov2019\midstages\sf_links_preprocessed.csv", index = False)
#Nodes
sf_refnodes = sf_links_noferry['REF_IN_ID'].to_list()
sf_nrefnodes = sf_links_noferry['NREF_IN_ID'].to_list()
sfnodes = sf_refnodes+ sf_nrefnodes
print(len(sfnodes))
sfnodes_unique = set(sfnodes)
len(set(sfnodes_unique))

new = all_nodes_noferry['geometry'].str.split(expand=True)
all_nodes_noferry['LON']= new[1].str[1:]
all_nodes_noferry['LAT']= new[2].str[:-1]

sf_nodes_noferry = all_nodes_noferry[all_nodes_noferry['NODE_ID'].isin(sfnodes_unique )]
len(sf_nodes_noferry)
#sf_nodes_noferry.to_csv("..\Nov2019\midstages\sf_nodes_preprocessed.csv", index = False)
#pop density
sf_pop = pd.read_csv("..\Nov2019\midstages\sf_popdensity.csv")
sf_pop_density = sf_pop[['NODE_ID','clippedghs']]
sf_pop_density.rename(columns = {'clippedghs':'pop_density'}, inplace = True)
#sf_pop_density.to_csv(r"C:\Users\anuku\GSR\UCBerkeley_GSR\Networks_Dataset\networks_dataset_Mobiliti\Nov2019\midstages\sfnodes_popdensity_preprocessed.csv", index = False)

# 2. LA SCAG
la_clip_geom = gpd.read_file("..\Nov2019\midstages\clip\la_clip.shp")
l = la_clip_geom['LINK_ID'].to_list()
la_links_noferry = all_links_noferry[all_links_noferry["LINK_ID"].isin(l)]
#check for ferry
s1_1 = la_links_noferry['LINK_ID'].to_list()
l2 = la_clip_geom[~la_clip_geom["LINK_ID"].isin(s1_1)] # these 164 are ferry links
#NODES
la_refnodes = la_links_noferry['REF_IN_ID'].to_list()
la_nrefnodes = la_links_noferry['NREF_IN_ID'].to_list()
lanodes = la_refnodes+ la_nrefnodes
lanodes_unique = set(lanodes)
la_nodes_noferry = all_nodes_noferry[all_nodes_noferry['NODE_ID'].isin(lanodes_unique)]
#la_nodes_noferry.to_csv("..\Nov2019\midstages\la_nodes_preprocessed.csv", index = False)
#pop density
la_pop_density = pd.read_csv("..\Nov2019\midstages\la_podensity.csv")
la_pop_density = la_pop[['NODE_ID','clippedghs']]
la_pop_density.rename(columns = {'clippedghs':'pop_density'}, inplace = True)
#la_pop_density.to_csv("..\Nov2019\midstages\lanodes_popdensity_preprocessed.csv", index = False)
