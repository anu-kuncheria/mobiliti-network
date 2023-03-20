"""
Tasks
1. Calculate length from shape nodes file
"""
import os
import pandas as pd
import numpy as np
import ast
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def stringtolist(string):
    lst = ast.literal_eval(string['nodes'])
    d=0
    for s,e in zip(lst[:-1],lst[1:]):
        d_= haversine(s[0],s[1],e[0],e[1])
        d+=d_
    return (d*1000)

if not os.path.isfile('../data/midstages/shapenodes_unidirec.csv'):
    cols_interest = ['LINK_ID', 'ST_NAME','REF_IN_ID', 'NREF_IN_ID', 'N_SHAPEPNT', 'FUNC_CLASS', 'SPEED_CAT','LANE_CAT','DIR_TRAVEL','PHYS_LANES','FROM_LANES','TO_LANES','geometry']
    all_links_ca = pd.read_csv('../data/midstages/all_links.csv', usecols = cols_interest)
    b1 = all_links_ca[all_links_ca['DIR_TRAVEL'] =='B']

    sn = pd.read_csv('../data/midstages/nav_street_for_mobiliti_links_shapenodes.csv', names = ['global_id','LINK_ID','nodes']) #shape nodes from Jane
    sn_bi = sn[sn['LINK_ID'].isin(b1['LINK_ID'].values)] #bidirec
    s2 = sn_bi.copy()
    s2['LINK_ID'] = np.arange(7000000000,7000000000+len(sn_bi))
    sn_FT = sn[~sn['LINK_ID'].isin(b1['LINK_ID'].values)]  #unidirec FT links
    shape_nodes_unidirec = sn_FT.append([s2,sn_bi])
    shape_nodes_unidirec = shape_nodes_unidirec.drop('global_id', axis = 1)
    shape_nodes_unidirec.to_csv('../data/midstages/shapenodes_unidirec.csv', index = False)


# Calculating length
shape_nodes = pd.read_csv('../data/midstages/shapenodes_unidirec.csv') 
shape_nodes['LENGTH(meters)'] = shape_nodes.apply(lambda string:stringtolist(string), axis = 1)
all_links_ca_uni  = pd.read_csv("../data/midstages/all_links_ca_uni_nolen.csv")
all_links_ca_uni_length = pd.merge(all_links_ca_uni,shape_nodes, on= 'LINK_ID')
#Check- all links with same PID has same links length
print(all_links_ca_uni_length.groupby(['PID','LENGTH(meters)'])['LINK_ID'].count().value_counts())

all_links_ca_uni_length_f = all_links_ca_uni_length[['LINK_ID','ST_NAME','REF_IN_ID','NREF_IN_ID','FUNC_CLASS','DIR_TRAVEL','NUM_PHYS_LANES','SPEED_KPH','CAPACITY','LENGTH(meters)','N_SHAPEPNT']]
all_links_ca_uni_length_f.rename(columns = {'CAPACITY':'CAPACITY(veh/hour)'}, inplace = True)
all_links_ca_uni_length_f.to_csv('../data/midstages/all_links_ca.csv', index = False)
