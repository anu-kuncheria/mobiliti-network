import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.geometry as geom
import filter_stronglyconnected as fst

def links_geom(links, nodes):
    geom_split = nodes['geometry'].str.split(expand=True)
    nodes['LON']= geom_split[1].str[1:].astype(float)
    nodes['LAT']= geom_split[2].str[:-1].astype(float)
    links['ref_lat'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['ref_long'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    links['nref_lat'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['nref_long'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    return links

def geom_shp(linksgeom, savepath = None):
    """
    Create shapefile from geom csv (CRS is GC WGS 84, epsg 4326)
    """
    linksgeom['geometry'] = linksgeom.apply(lambda x: geom.LineString([(x['ref_long'], x['ref_lat']) , (x['nref_long'], x['nref_lat'])]), axis = 1)
    linksgeom_gdf = gpd.GeoDataFrame(linksgeom, geometry = linksgeom.geometry)
    linksgeom_gdf.set_crs(epsg=4326, inplace=True)
    linksgeom_gdf.to_file(os.path.join(savepath, 'alllinksgeom_gdf.shp'), driver='ESRI Shapefile')

def process_boundary(taz_boundary_path):
    taz_shapefile = gpd.read_file(taz_boundary_path)
    if not taz_shapefile.crs ==  'EPSG:4326' :
        taz_shapefile = taz_shapefile.to_crs(4326) 

    # select the columns that you with to use for the dissolve and that will be retained
    taz_dissolve = taz_shapefile[['geometry']].dissolve()
    taz_square = taz_dissolve['geometry'].envelope
    bufferlength = taz_square.length/50 # buffer width
    taz_buffer = taz_square.buffer(bufferlength)

    fig, ax = plt.subplots(figsize = (10,8)) 
    taz_buffer.plot(ax = ax, alpha = 0.1, color = 'orange')
    taz_square.plot(ax = ax, alpha = 0.3)
    taz_dissolve.plot(ax = ax)
    plt.show()
    return taz_buffer

def clip_links(links, boundary_shp):
    assert links.crs == boundary_shp.crs, "CRS doesnt match. links CRS: {}, boundary CRS: {}".format(links.crs,boundary_shp.crs)
    clippedlinks = gpd.clip(links, boundary_shp)
    return clippedlinks

def full_connected_filter(nodes_path,links_path):
    nodes, links = fst.read_nodes(nodes_path), fst.read_links(links_path)
    nodes_b, links_b = fst.keep_largest_scc(nodes, links) #new set
    nodes_diff = fst.diff_nodes(nodes, nodes_b)
    links_diff = fst.diff_links(links, links_b)
    n_id_diff = []
    for i in range(0, len(nodes_diff)):
        n_id_diff.append(nodes_diff[i].NODE_ID)
    l_id_diff = []
    for i in range(0, len(links_diff)):
        l_id_diff.append(links_diff[i].LINK_ID)

    # removing the not connected link and node ids found above to the final file
    nodes_pre = pd.read_csv(nodes_path)
    links_pre = pd.read_csv(links_path)
    links_post = links_pre[~links_pre['LINK_ID'].isin(l_id_diff)]
    nodes_post = nodes_pre[~nodes_pre['NODE_ID'].isin(n_id_diff)]
    print("Links number processed:", len(links_post))
    print("Nodes number processed:", len(nodes_post))
    return links_post, nodes_post

def write_file(df, savepath, savename):
    df.to_csv(os.path.join(savepath, savename), index = False)













