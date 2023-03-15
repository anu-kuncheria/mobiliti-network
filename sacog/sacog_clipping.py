import pandas as pd
import geopandas as gpd
import os
import shapely.geometry as geom

def links_geom(links, nodes):
    geom_split = nodes['geometry'].str.split(expand=True)
    nodes['LON']= geom_split[1].str[1:].astype(float)
    nodes['LAT']= geom_split[2].str[:-1].astype(float)
    links['ref_lat'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['ref_long'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    links['nref_lat'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['nref_long'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    return links

def geom_shp(linksgeom, savename = None):
    """
    Create shapefile from geom csv (CRS is GC WGS 84, epsg 4326)
    """
    linksgeom['geometry'] = linksgeom.apply(lambda x: geom.LineString([(x['ref_long'], x['ref_lat']) , (x['nref_long'], x['nref_lat'])]), axis = 1)
    linksgeom_gdf = gpd.GeoDataFrame(linksgeom, geometry = linksgeom.geometry)
    linksgeom_gdf.set_crs(epsg=4326, inplace=True)
    return linksgeom_gdf

def clip_links(links, boundary_shp):
    assert links.crs == boundary_shp.crs, "CRS doesnt match. links CRS: {}, boundary CRS: {}".format(links.crs,boundary_shp.crs)
    clippedlinks = gpd.clip(links, boundary_shp)
    return clippedlinks


#1.Clipping
commonpath = '../Networks_Dataset' 
alllinks = pd.read_csv(os.path.join(commonpath, 'networks_dataset_Mobiliti/Nov2019/for_drive/July2021/all_links.csv')) # latest links edited
allnodes = pd.read_csv(os.path.join(commonpath, 'networks_dataset_Mobiliti/Nov2019/for_drive/all_nodes.csv'))
clipboundarypath = gpd.read_file(os.path.join(commonpath,'sacog_region/data/sacog_boundary_rectangle_epsg4326.shp' )) # rectangular boundary generated in ArcGIS
print("Links, Nodes, Boundary shapes are ...")
print(alllinks.shape, allnodes.shape, clipboundarypath.shape)

alllinksgeom = links_geom(alllinks, allnodes)
alllinksgeom_gdf = geom_shp(alllinksgeom, savename = None)
alllinks_clipped = clip_links(alllinksgeom_gdf,clipboundarypath)
print("Clipped links shape is..", alllinks_clipped.shape)
#alllinks_clipped.to_file("sacog_links.geojson", driver = 'GeoJSON')

#write to file
#links
alllinks_clipped[['LINK_ID', 'ST_NAME', 'REF_IN_ID', 'NREF_IN_ID', 'FUNC_CLASS',
       'DIR_TRAVEL', 'NUM_PHYS_LANES', 'SPEED_KPH', 'LENGTH(meters)',
       'CAPACITY(veh/hour)', 'RAMP']].to_csv("../mid_processing/sacog_links_preprocess.csv", index = False)

#nodes
sac_refnodes = alllinks_clipped['REF_IN_ID'].to_list()
sac_nrefnodes = alllinks_clipped['NREF_IN_ID'].to_list()
sacnodes = sac_refnodes+ sac_nrefnodes
sacnodes_unique = set(sacnodes)
nodes = allnodes[allnodes['NODE_ID'].isin(sacnodes_unique)]
print(len(nodes))
nodes['geom'] = nodes['geometry'] #reductant column -making it so that it is consistent with other networks generated
nodes.to_csv("mid_processing/sacog_nodes_preprocess.csv", index = False)
