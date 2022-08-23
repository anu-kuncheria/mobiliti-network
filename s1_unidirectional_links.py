#Tasks
#1. Convert bi-directional to uni-directional links
#2. Calculate the number of lanes from multiple rule based decisions based on here documentation

import pandas as pd
import numpy as np
import geopandas as gpd
'''
Raw File Preprocessing:
#California links combined from here - 3Million Links
streets1 = gpd.read_file('../here_map_11/here_map_11_shapefiles/Streets.shp')
streets2 = gpd.read_file('../here_map_12-20191207T191053Z-001/here_map_12/here_map_12_shapefiles/Streets.shp')
streets3 = gpd.read_file('../here_map_13/here_map_13_shapefiles/Streets.shp')
streets4 = gpd.read_file('../here_map_14/here_map_14_shapefiles/Streets.shp')
streets5 = gpd.read_file('../here_map_15-20191207T193135Z-001/here_map_15\here_map_15_shapefiles/Streets.shp')
links = streets1.append(streets2, sort=False)
links = links.append(streets3,sort=False)
links = links.append(streets4,sort=False )
links = links.append(streets5,sort=False )
links.to_csv('../midstages/all_links.csv')

# LANES.dbf file Pg 246, pg 643
from simpledbf import Dbf5
lanes1 = Dbf5('../here_map_11/here_map_11_shapefiles/Lane.dbf')
lanes2 = Dbf5('../here_map_12-20191207T191053Z-001/here_map_12/here_map_12_shapefiles/Lane.dbf')
lanes3 = Dbf5('../here_map_13/here_map_13_shapefiles/Lane.dbf')
lanes4 = Dbf5('../here_map_14/here_map_14_shapefiles/Lane.dbf')
lanes5 = Dbf5('../here_map_15-20191207T193135Z-001/here_map_15/here_map_15_shapefiles/Lane.dbf')
lanes_df1 = lanes1.to_dataframe()
lanes_df2 = lanes2.to_dataframe()
lanes_df3 = lanes3.to_dataframe()
lanes_df4 = lanes4.to_dataframe()
lanes_df5 = lanes5.to_dataframe()
lanes_df = lanes_df1.append(lanes_df2)
lanes_df = lanes_df.append(lanes_df3)
lanes_df = lanes_df.append(lanes_df4)
lanes_df = lanes_df.append(lanes_df5)
lanes_df.to_csv('...midstages/lanes_df.csv')
'''
#Reading in data
here_links = pd.read_csv('../midstages/all_links.csv')
all_links_ca = here_links[['LINK_ID', 'ST_NAME','REF_IN_ID', 'NREF_IN_ID', 'N_SHAPEPNT', 'FUNC_CLASS', 'SPEED_CAT','LANE_CAT','DIR_TRAVEL','PHYS_LANES','FROM_LANES','TO_LANES','geometry']]
lanes_df = pd.read_csv('../midstages/lanes_df.csv')

#Transformations
#1. Converting bidirectional links to unidirectional F
uni_F = all_links_ca[all_links_ca['DIR_TRAVEL'] =='F'] #divide links rows into F,T,B
uni_T = all_links_ca[all_links_ca['DIR_TRAVEL'] =='T']
b1 = all_links_ca[all_links_ca['DIR_TRAVEL'] =='B']
#creating a PID for b1
b1['PID'] = np.arange(0,len(b1))
b2 = b1.copy()   #new df for b2
b2['partner_LINK_ID'] = np.arange(7000000000,7000000000+len(b2))
#changing the directions for B
b1['DIR_TRAVEL'] = 'F'
b2['DIR_TRAVEL'] = 'T'

# Deciding the physical lanes
bi_dir_phylanes_zero = here_links[(here_links['DIR_TRAVEL']=='B') & (here_links['PHYS_LANES']== 0) ]
bi_phylzero_lanecat2 = bi_dir_phylanes_zero[bi_dir_phylanes_zero['LANE_CAT']==2][['LINK_ID','PHYS_LANES','TO_LANES','FROM_LANES']]
bi_phylzero_lanecat3 = bi_dir_phylanes_zero[bi_dir_phylanes_zero['LANE_CAT']==3][['LINK_ID','PHYS_LANES','TO_LANES','FROM_LANES']]
bi_dir_phylanes_notzero = here_links[(here_links['DIR_TRAVEL']=='B') & (here_links['PHYS_LANES'] != 0) ]
bi_dir_phylanes_fromlanes_notzero = bi_dir_phylanes_notzero[bi_dir_phylanes_notzero['FROM_LANES']!=0]
print(f"Total birectional links: {len(here_links[here_links['DIR_TRAVEL']=='B'])}")
print(f"Out of the total birectional, links with physical lanes not 0: {len(bi_dir_phylanes_notzero)}")
print(f"Out of these,fromlane not 0: {len(bi_dir_phylanes_fromlanes_notzero )}")
print(f"Physical lanes manually determined by me : {len(bi_dir_phylanes_notzero) - len(bi_dir_phylanes_fromlanes_notzero )}")

lanes_df_bi = lanes_df[lanes_df.LINK_ID.isin(bi_dir_phylanes_notzero.LINK_ID)]
a = lanes_df_bi.groupby(['LINK_ID','DIR_TRAV'])['LANE_ID'].count().reset_index() #IMPORTNT- used later
a1 = a[a['DIR_TRAV']== 'F'] #number of phy lanes in F direc
a2 = a[a['DIR_TRAV']== 'T']
a1.rename(columns = {'LANE_ID':'count'}, inplace = True)
a2.rename(columns = {'LANE_ID':'count'}, inplace = True)

#Set1: PHYS_LANES not 0
# creating num_phy_lanes for PHYS_LANES !=0 from lane.dbf file from a1 and a2 created above from lanes dbf file
b1 = pd.merge(b1, a1[['LINK_ID','count']], on="LINK_ID", how = 'left')
b2 = pd.merge(b2, a2[['LINK_ID','count']], on="LINK_ID", how = 'left')
#Set2: PHYS_LANES equals 0
def num_phys(row):
    if row['PHYS_LANES']== 0:
        if row['DIR_TRAVEL']== 'F':
            if row['FROM_LANES']==0:
                if row['LANE_CAT'] == 1:
                    row['count'] = 1
                elif row['LANE_CAT'] == 2:
                    row['count'] = 2
                elif row['LANE_CAT'] == 3:
                    row['count'] = 4
            else:row['count'] = row['FROM_LANES']

        elif row['DIR_TRAVEL']== 'T':
            if row['TO_LANES']==0:
                if row['LANE_CAT'] == 1:
                    row['count'] = 1
                elif row['LANE_CAT'] == 2:
                    row['count'] = 2
                elif row['LANE_CAT'] == 3:
                    row['count'] = 4
            else:row['count'] = row['TO_LANES']
    return row['count']

b1['count'] = b1.apply(lambda row:num_phys(row), axis=1)
b2['count'] = b2.apply(lambda row:num_phys(row), axis=1)

#Create partner link ids
partners_links = b2[['PID','LINK_ID','partner_LINK_ID']] #LINKS PARTNERS FOR BI DIRECTIONAL
partners_links.to_csv("..\midstages\partner_link_ids.csv", index = False)

b2.drop(columns = 'LINK_ID', inplace = True)
b2.rename(columns = {'partner_LINK_ID': 'LINK_ID'}, inplace = True)
b2 = b2[['LINK_ID','ST_NAME', 'REF_IN_ID', 'NREF_IN_ID', 'N_SHAPEPNT', 'FUNC_CLASS',
       'SPEED_CAT', 'LANE_CAT', 'DIR_TRAVEL', 'PHYS_LANES', 'FROM_LANES',
       'TO_LANES', 'geometry', 'PID','count' ]]
b2['ref'] = b2['NREF_IN_ID']
b2['nref'] = b2['REF_IN_ID']
b2['DIR_TRAVEL']= 'F'
b2.drop(['REF_IN_ID','NREF_IN_ID'], axis = 1, inplace = True)
b2.rename(columns = {'ref':'REF_IN_ID','nref':'NREF_IN_ID'}, inplace = True)

# 2. Unidirectional links to F
uni_F['count'] = uni_F['PHYS_LANES']
uni_T['count'] = uni_T['PHYS_LANES']
uni_F['count'] = uni_F.apply(lambda row:num_phys(row), axis=1) #NO lanes with 0 num of phys lanes
uni_T['count'] = uni_T.apply(lambda row:num_phys(row), axis=1)
#chnaging the direction for T
uni_T['ref'] = uni_T['NREF_IN_ID']
uni_T['nref'] = uni_T['REF_IN_ID']
uni_T['DIR_TRAVEL']= 'F'
uni_T.drop(['REF_IN_ID','NREF_IN_ID'], axis = 1, inplace = True)
uni_T.rename(columns = {'ref':'REF_IN_ID','nref':'NREF_IN_ID'}, inplace = True)

#3. Append 4 dataframes
all_links_ca_uni = b1.append(b2)
all_links_ca_uni = all_links_ca_uni.append(uni_F)
all_links_ca_uni = all_links_ca_uni.append(uni_T)

# 4. Sanity Checks
def check1(links_df):
    print('No of tear drops are:', links_df[links_df['REF_IN_ID'] == links_df['NREF_IN_ID']]['LINK_ID'].count())
def check2(links_df):
    print('No of links with same ref and nref node ids:', links_df['REF_IN_ID'].equals(links_df['NREF_IN_ID'])*1)
def check3(links_df):
    return links_df.isnull().sum()

#5. Write the modified file
all_links_ca_uni.rename(columns = {'count':'NUM_PHYS_LANES'}, inplace= True)
all_links_ca_uni.to_csv('../midstages/mid_uni_links_correctphyslane.csv', index = False)