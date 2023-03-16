"""
Tasks
1. Calculate free speed and capacity for links
"""
import pandas as pd
import numpy as np
import geopandas as gpd

def speed(row):
    return speed_cat[int(row['SPEED_CAT'])]
def capacity(row):
    return capac[int(row['SPEED_CAT'])]

speed_cat = {1:130, 2:115, 3:95, 4:80,5:60,6:40,7:20,8:5} #free speed based on HERE speed category values
capac = {1:2000, 2:2000, 3:2000,4:1500, 5:1500, 6:1000, 7:600,8:300} # capacities based on HERE speed categories and Matsim reference

all_links_ca_uni = pd.read_csv('../midstages/mid_uni_links_correctphyslane.csv')
all_links_ca_uni['SPEED_KPH'] = all_links_ca_uni.apply(lambda row:speed(row), axis = 1)
all_links_ca_uni['CAPACITY'] = all_links_ca_uni.apply(lambda row:capacity(row), axis=1)
all_links_ca_uni['CAPACITY'] = all_links_ca_uni['CAPACITY'] * all_links_ca_uni['NUM_PHYS_LANES']
all_links_ca_uni.to_csv("../midstages/all_links_ca_uni_nolen.csv", index = False)
