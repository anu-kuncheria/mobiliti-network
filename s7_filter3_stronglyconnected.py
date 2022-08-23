#Tasks
#Apply Cy's strongly connected filter to the clipped network.
import sys
import os
import csv
import itertools

class Node(object):
  __slots__ = ["NODE_ID", "LAT", "LON"]
  def __init__(self,NODE_ID, LAT, LON):
    self.NODE_ID = NODE_ID
    self.LAT = LAT
    self.LON = LON

def read_nodes(node_file):
  print("Loading nodes ...")
  with open(node_file) as f:
    lines = f.readlines()
  node_n = len(lines) - 1 # ignore header line
  print("Parsing %d nodes ..." % node_n)
  nodes = []
  for l in lines[1:]:
    l = l.strip()
    entry = l.split(",")
    node_id = int(entry[0])
    # ignore entries 1 and 2 (redundant geometry)
    lon = float(entry[2])
    lat = float(entry[3])
    nodes.append(Node(node_id, lat, lon))
  return nodes

class Link(object):
  __slots__ = ['LINK_ID', 'ST_NAME', 'REF_IN_ID', 'NREF_IN_ID','FUNC_CLASS','NUM_PHYS_LANES', 'SPEED_KPH', 'CAPACITY','LENGTH', 'N_SHAPEPNT']
  def __init__(self, LINK_ID, ST_NAME, REF_IN_ID, NREF_IN_ID,
               FUNC_CLASS, NUM_PHYS_LANES, SPEED_KPH, CAPACITY,LENGTH, N_SHAPEPNT):
    self.LINK_ID = LINK_ID
    self.ST_NAME = ST_NAME
    self.REF_IN_ID = REF_IN_ID
    self.NREF_IN_ID = NREF_IN_ID
    self.FUNC_CLASS = FUNC_CLASS
    self.NUM_PHYS_LANES = NUM_PHYS_LANES
    self.SPEED_KPH =SPEED_KPH
    self.CAPACITY = CAPACITY
    self.LENGTH = LENGTH
    self.N_SHAPEPNT= N_SHAPEPNT

def csv_split(s):
  return list(csv.reader([s], skipinitialspace=True))[0]

def read_links(link_file):
  print("Loading links ...")
  with open(link_file,encoding="utf8", mode='r') as f:
    lines = f.readlines()
  link_n = len(lines) - 1 # ignore header line
  print("Parsing %d links ..." % link_n)
  links = []
  for l in lines[1:]:
    entry = csv_split(l.strip())
    link_id = int(entry[0])
    name    = entry[1]
    src     = int(entry[2]) #startnode
    dst     = int(entry[3]) #end node
    fc      = int(entry[4]) #fc
    assert entry[5] == "F" # forward direction
    lanes   = int(float(entry[6]))
    speed   = float(entry[7]) * 1000 / (60 * 60) # convert km/h to m/s
    cap     = int(float(entry[8]))
    length  = float(entry[9])
    shape_node_n = int(entry[10])
    links.append(Link(link_id,name,src, dst,fc,lanes,speed,cap,length,shape_node_n))
  return links

def filter_nodes(nodes, keep_ids):
  keep_ids_set = set(keep_ids)
  return [n for n in nodes if n.NODE_ID in keep_ids_set]

def filter_links(links, keep_ids):
  keep_ids_set = set(keep_ids)
  return [l for l in links if l.REF_IN_ID in keep_ids_set and l.NREF_IN_ID in keep_ids_set]

def get_valid_links(links, nodes):
  print("Filtering out invalid links ...")
  result = filter_links(links, [n.NODE_ID for n in nodes])
  print("Number of valid links: %d of %d" % (len(result), len(links)))
  return result

def keep_largest_scc(nodes, links):
  print("Initializing digraph ...")
  G = networkx.DiGraph()
  for n in nodes:
    G.add_node(n.NODE_ID)
  for l in links:
    G.add_edge(l.REF_IN_ID, l.NREF_IN_ID)

  print("Computing strongly connected components ...")
  sccs = list(networkx.strongly_connected_components(G))
  print("Sizes of strongly connected components:", sorted(map(len, sccs), reverse=True))
  max_scc = max(sccs, key=len)

  print("Filtering nodes and links in largest component:", len(max_scc))
  nodes = filter_nodes(nodes, max_scc)
  links = filter_links(links, max_scc)
  print("Keeping %d nodes and %d links ..." % (len(nodes), len(links)))
  return (nodes, links)

def create_node_gdf(nodes):
  print("Creating node GDF ...")
  df = pandas.DataFrame( \
      {"ids": [n.NODE_ID for n in nodes], \
       "coordinates": [shapely.geometry.Point((n.LON, n.LAT)) for n in nodes]})
  gdf = geopandas.GeoDataFrame(df, geometry = "coordinates")
  gdf.crs = {"init": "epsg:4326"}
  print("Converting nodes to epsg:26910 coordinate system ...")
  gdf.to_crs({"init": "epsg:26910"}, inplace = True)
  return gdf

def write_nodes_lat_lon_x_y(filename, nodes, node_gdf):
  assert node_gdf.shape[0] == len(nodes)
  f = open(filename, "w")
  f.write("id,lat,lon,x,y\n")
  f.write("%d\n" % len(nodes))
  for (i, n) in enumerate(nodes):
    assert node_gdf["ids"].iloc[i] == n.NODE_ID
    x = node_gdf.geometry.iloc[i].x
    y = node_gdf.geometry.iloc[i].y
    f.write("%d,%.7f,%.7f,%.7f,%.7f\n" % (n.node_id, n.lat, n.lon, x, y))

def write_nodes_dens(filename, nodes):
  f = open(filename, "w")
  f.write("id,density\n")
  f.write("%d\n" % len(nodes))
  for n in nodes:
    f.write("%d,%g\n" % (n.node_id, n.dens))

def write_links(filename, links):
  f = open(filename, "w")
  f.write("id,src,dst,capacity,lanes,length,freespeed\n")
  f.write("%d\n" % len(links))
  for l in links:
    f.write("%d,%d,%d,%d,%d,%g,%g\n" % (l.link_id, l.src, l.dst, l.cap, l.lanes, l.length, l.speed))

def create_link_gdf(links, nodes):
  print("Creating link GDF ...")
  # create node dict
  nodes_by_id = {}
  for n in nodes:
    assert n.node_id not in nodes_by_id
    nodes_by_id[n.node_id] = n

  def get_xy(node_id):
    n = nodes_by_id[node_id]
    return (float(n.lon), float(n.lat))

  segments = [(get_xy(l.src), get_xy(l.dst)) for l in links]
  df = pandas.DataFrame(
      {"id": [l.link_id for l in links],
       "segments": map(shapely.geometry.LineString, segments)})

  gdf = geopandas.GeoDataFrame(df, geometry = "segments")
  gdf.crs = {"init": "epsg:4326"}
  print("Converting links to epsg:26910 coordinate system ...")
  gdf.to_crs({"init": "epsg:26910"}, inplace=True)

  return gdf


def diff_nodes(nodes_a, nodes_b):
  nodes_b_id_set = set([n.NODE_ID for n in nodes_b])
  return [n for n in nodes_a if n.NODE_ID not in nodes_b_id_set]

def diff_links(links_a, links_b):
  links_b_id_set = set([l.LINK_ID for l in links_b])
  return [l for l in links_a if l.LINK_ID not in links_b_id_set]

def main(args):
  flag_plot_map = bool(int(os.getenv("plot_map", False)))

  (in_node_file, in_link_file) = args[1:3]
  orig_nodes = read_nodes(in_node_file)
  orig_links = read_links(in_link_file)
  orig_links = get_valid_links(orig_links, orig_nodes)

  (nodes, links) = keep_largest_scc(orig_nodes, orig_links)

  if flag_plot_map:
    del_nodes = diff_nodes(orig_nodes, nodes)
    del_links = diff_links(orig_links, links)
    del_node_gdf = create_node_gdf(del_nodes)
    del_link_gdf = create_link_gdf(del_links, orig_nodes)
    new_link_gdf = create_link_gdf(links, nodes)
    base = del_node_gdf.plot(color = "red", markersize = 2)
    del_link_gdf.plot(ax = base, color =  "red", linewidths = [l.lanes for l in del_links])
    new_link_gdf.plot(ax = base, color = "gray", linewidths = [l.lanes for l in links])
    plt.show()
  else:
    node_gdf = create_node_gdf(nodes)
    (out_node_file, out_dens_file, out_link_file) = args[3:6]
    write_nodes_lat_lon_x_y(out_node_file, nodes, node_gdf)
    write_nodes_dens(out_dens_file, nodes)
    write_links(out_link_file, links)

#Main - apply to our network
def full_connected_filter(path1,path2,path3,savename):
    nodes_a = read_nodes(path1)
    links_a = read_links(path2)
    nodes_b, links_b = keep_largest_scc(nodes_a, links_a) #new set
    nodes_diff = diff_nodes(nodes_a, nodes_b)
    links_diff = diff_links(links_a, links_b)
    n_id_diff = []
    for i in range(0, len(nodes_diff)):
        n_id_diff.append(nodes_diff[i].NODE_ID)
    l_id_diff = []
    for i in range(0, len(links_diff)):
        l_id_diff.append(links_diff[i].LINK_ID)
    # removing the not connecetd links and nodes found above to the final file i have
    nodes_pre = pd.read_csv(path1)
    links_pre = pd.read_csv(path2)
    popdensity = pd.read_csv(path3)
    links_post = links_pre[~links_pre['LINK_ID'].isin(l_id_diff)]
    nodes_post = nodes_pre[~nodes_pre['NODE_ID'].isin(n_id_diff)]
    popdensity_post = popdensity[~popdensity['NODE_ID'].isin(n_id_diff)]
    print("Links number processed:", len(links_post))
    print("Nodes number processed:", len(nodes_post))
    print("Popdensity Nodes number processed:", len(popdensity_post))
    #writing the final to csv
    links_post.to_csv("../midtsages/{}_links.csv".format(savename), index = False)
    nodes_post.to_csv("../midstages/{}_nodes.csv".format(savename), index = False)
    popdensity_post.to_csv("../midstages/{}_popdensity.csv".format(savename), index = False)

# Bay Area
path1 = "../midstages/sf_nodes_preprocessed_accessrest.csv"
path2 = "../midstages/sf_links_preprocessed_accessrest.csv"
path3 = "../midstages/sf_popdensity_preprocessed_accessrest.csv"
full_connected_filter(path1,path2,path3,"sf")
#LA Scag
path1 = "../midstages/la_nodes_preprocessed_accessrest.csv"
path2 = "../midstages/la_links_preprocessed_accessrest.csv"
path3 = "../midstages/la_popdensity_preprocessed_accessrest.csv"
full_connected_filter(path1,path2,path3,"la")
