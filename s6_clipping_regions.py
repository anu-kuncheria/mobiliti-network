import pandas as pd
import numpy as np
import geopandas as gpd

#Tasks
#1. Clip SF Bay Area
#2. Clip LA SCAG Region

all_nodes_noferry = pd.read_csv("\Nov2019\for_drive\all_nodes_noferry.csv")
all_links_noferry = pd.read_csv("\Nov2019\for_drive\all_links_noferry.csv")
new = all_nodes_noferry['geometry'].str.split(expand=True)
all_nodes_noferry['LON']= new[1].str[1:]
all_nodes_noferry['LAT']= new[2].str[:-1]

def clip(clipath,popdensitypath, savename):
    clip_geom = gpd.read_file(clipath) #shapefile
    a = clip_geom['LINK_ID'].to_list()
    links_noferry = all_links_noferry[all_links_noferry["LINK_ID"].isin(a)]
    refnodes = links_noferry['REF_IN_ID'].to_list()
    nrefnodes = links_noferry['NREF_IN_ID'].to_list()
    citynodes = refnodes+ nrefnodes
    citynodes_unique = set(citynodes)
    city_nodes_noferry = all_nodes_noferry[all_nodes_noferry['NODE_ID'].isin(citynodes_unique )]
    city_pop = pd.read_csv(popdensitypath)
    city_pop_density = city_pop[['NODE_ID','clippedghs']]
    city_pop_density.rename(columns = {'clippedghs':'pop_density'}, inplace = True)

    city_nodes_noferry.to_csv("{}_nodes_preprocessed.csv".format(savename), index = False)
    links_noferry.to_csv("{}_links_preprocessed.csv".format(savename), index = False)
    city_pop_density.to_csv("{}_popdensity_preprocessed.csv".format(savename), index = False)

# 1. SF Bay Area
print("Clipping Sf Bay Area ...")
clipath = "..\Nov2019\midstages\clip\SF_Clip.shp"
popdensitypath = "..\Nov2019\midstages\sf_popdensity.csv"
clip(clipath,popdensitypath,'sf')

# 2. LA Scag
print("Clipping LA Scag Region ...")
clipath = "..\Nov2019\midstages\clip\la_clip.shp"
popdensitypath = "..\Nov2019\midstages\la_podensity.csv"
clip(clipath,popdensitypath,'la')
