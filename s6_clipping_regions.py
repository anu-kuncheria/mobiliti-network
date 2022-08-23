#Tasks
#1. Clip SF Bay Area
#2. Clip LA SCAG Region

import pandas as pd
import numpy as np
import geopandas as gpd

def clip(clipboundarypath, popdensitypath, savename, links = all_links_noferry, nodes = all_nodes_noferry):
    """
    Input -> Boundary shapefile, Population Density file, 
    Output -> Nodes, Links, Population Density csv 
    """
    clip_geom = gpd.read_file(clipboundarypath) #shapefile for the clipping region
    a = clip_geom['LINK_ID'].to_list()
    links_noferry = links[links["LINK_ID"].isin(a)]
    refnodes = links_noferry['REF_IN_ID'].to_list()
    nrefnodes = links_noferry['NREF_IN_ID'].to_list()
    citynodes = refnodes+ nrefnodes
    citynodes_unique = set(citynodes)
    city_nodes_noferry = nodes[nodes['NODE_ID'].isin(citynodes_unique)]
    city_pop = pd.read_csv(popdensitypath)
    city_pop_density = city_pop[['NODE_ID','clippedghs']]
    city_pop_density.rename(columns = {'clippedghs':'pop_density'}, inplace = True)

    #Write Files 
    city_nodes_noferry.to_csv("{}_nodes_preprocessed.csv".format(savename), index = False)
    links_noferry.to_csv("{}_links_preprocessed.csv".format(savename), index = False)
    city_pop_density.to_csv("{}_popdensity_preprocessed.csv".format(savename), index = False)


#All links and nodes
all_nodes_noferry = pd.read_csv("../midstages/all_nodes_noferry_thrufilter.csv")
all_links_noferry = pd.read_csv("../midstages/all_links_noferry_thrufilter.csv")
new = all_nodes_noferry['geometry'].str.split(expand=True)
all_nodes_noferry['LON']= new[1].str[1:]
all_nodes_noferry['LAT']= new[2].str[:-1]

# 1. SF Bay Area
print("Clipping Sf Bay Area ...")
clipboundarypath = "../midstages/clip/SF_Clip.shp"
popdensitypath = "../midstages/sf_popdensity.csv"
clip(clipboundarypath, popdensitypath, savename = 'sf', links = all_links_noferry, nodes = all_nodes_noferry)

# 2. LA SCAG
print("Clipping LA Scag Region ...")
clipath = "../midstages/clip/la_clip.shp"
popdensitypath = "../midstages/la_podensity.csv"
clip(clipboundarypath, popdensitypath, savename = 'la', links = all_links_noferry, nodes = all_nodes_noferry)


