import pandas as pd
import numpy as np
import geopandas as gpd
import ast

#Tasks
#1. Calculate length from shape nodes file

'''
# Length is to be calculated from shapenodes. But shapenodes for B,F,T links
sn = pd.read_csv('nav_street_for_mobiliti_links_shapenodes.csv', names = ['global_id','LINK_ID','nodes'])
sn.head(5)  # link id and shape nodes for each link
#create additional links in shape nodes column
sn_bi = sn[sn['LINK_ID'].isin(b1['LINK_ID'].values)] #bidirec
len(sn_bi)
s2 = sn_bi.copy()
s2['LINK_ID'] = np.arange(7000000000,7000000000+len(sn_bi))
sn_FT = sn[~sn['LINK_ID'].isin(b1['LINK_ID'].values)]  #unidirec FT links
shape_nodes_unidirec = sn_FT.append([s2,sn_bi])
len(shape_nodes_unidirec)
shape_nodes_unidirec = shape_nodes_unidirec.drop('global_id', axis = 1)
#shape_nodes_unidirec.to_csv('\networks_dataset_Mobiliti\Nov2019\shapenodes_unidirec.csv', index = False)
'''

shape_nodes = pd.read_csv('\networks_dataset_Mobiliti\Nov2019\midstages\shapenodes_unidirec.csv')
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
def stringtolist(string):
    '''Convert shapenodes string to list
    '''
    lst = ast.literal_eval(string['nodes'])
    d=0
    for s,e in zip(lst[:-1],lst[1:]):
        d_= haversine(s[0],s[1],e[0],e[1])
#         print (s,e,d_)
        d+=d_
    return (d*1000)

shape_nodes['LENGTH(meters)'] = shape_nodes.apply(lambda string:stringtolist(string), axis = 1)
shape_nodes.to_csv("../midstages/shapenodes_linklength.csv", index = False)

# adding link length to all links from the shapenodes calcuated
all_links_ca_uni  = pd.read_csv("all_links_ca_uni_nolen.csv")
all_links_ca_uni_length = pd.merge(all_links_ca_uni,shape_nodes, on= 'LINK_ID')
#CHECK-  all links with same PID has same links length
all_links_ca_uni_length.groupby(['PID','LENGTH(meters)'])['LINK_ID'].count().value_counts()

#Filter for final save
all_links_ca_uni_length_f = all_links_ca_uni_length[['LINK_ID','ST_NAME','REF_IN_ID','NREF_IN_ID','FUNC_CLASS','DIR_TRAVEL','NUM_PHYS_LANES','SPEED_KPH','CAPACITY','LENGTH(meters)','N_SHAPEPNT']]
all_links_ca_uni_length_f.rename(columns = {'CAPACITY':'CAPACITY(veh/hour)'}, inplace = True)
all_links_ca_uni_length_f.to_csv('\Nov2019\all_links_ca.csv', index = False)
