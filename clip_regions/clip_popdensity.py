import os
import pandas as pd
import numpy as np
import yaml
import rasterio
from pyproj import Transformer
import filter_clipregions as fcr

config_file = "config.yaml"
a_yaml_file = open(config_file)
config = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

raster_path = config["popdensity"]["raster"]
popdensity_name = config["popdensity"]["popdensity_filename"]
savepath_final = config["write"]["savepath_final"]
nodesname = config["write"]["nodes_filename"]
cityname = config["write"]["cityname"]


def extract_raster_value( lon, lat, raster_path):
    with rasterio.open(raster_path) as rds:
        transformer = Transformer.from_crs("EPSG:4326", rds.crs, always_xy=True)  # convert coordinate to raster projection
        xx, yy = transformer.transform(lon, lat)
        value = list(rds.sample([(xx, yy)]))[0] # get value from grid
        return value

    
clipped_nodes = pd.read_csv(os.path.join(savepath_final, cityname + '_' + nodesname))
print("===== Extracting the raster values to nodes ======")
clipped_nodes['popdensity'] = clipped_nodes.apply(lambda x: extract_raster_value(x['LON'], x['LAT'],raster_path), axis = 1)
#replace negavtive values with 0. These are null values in tiff
clipped_nodes['popdensity'] = np.where(clipped_nodes['popdensity']<0, 0, clipped_nodes['popdensity'])

fcr.write_file(clipped_nodes[['NODE_ID', 'popdensity']], savepath= savepath_final, savename = cityname + '_' + popdensity_name )







