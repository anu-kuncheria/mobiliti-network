#Tasks
#1. Get speed values
#2. Get capacity values

import pandas as pd
import numpy as np
import geopandas as gpd

#Attribute 1 - Defining Free speed
speed_cat = {1:130, 2:115, 3:95, 4:80,5:60,6:40,7:20,8:5}
def speed(row):
    return speed_cat[int(row['SPEED_CAT'])]

# Attribute 2 - Capacities based on speed categories and Matsim reference
capac = {1:2000, 2:2000, 3:2000,4:1500, 5:1500, 6:1000, 7:600,8:300}
def capacity(row):
    return capac[int(row['SPEED_CAT'])]

all_links_ca_uni = pd.read_csv('../midstages/mid_uni_links_correctphyslane.csv')
all_links_ca_uni['SPEED_KPH'] = all_links_ca_uni.apply(lambda row:speed(row), axis = 1)
all_links_ca_uni['CAPACITY'] = all_links_ca_uni.apply(lambda row:capacity(row), axis=1)
all_links_ca_uni['CAPACITY'] = all_links_ca_uni['CAPACITY'] * all_links_ca_uni['NUM_PHYS_LANES']
all_links_ca_uni.to_csv("../midtages/all_links_ca_uni_nolen.csv", index = False)
