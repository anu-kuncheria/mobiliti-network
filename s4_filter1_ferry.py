"""
Tasks
1.Filter out ferry links
"""

import pandas as pd
import numpy as np

all_links_ca_uni_length_f = pd.read_csv('../midstages/all_links_ca.csv')
partner_links = pd.read_csv("../midstages/partner_link_ids.csv")
all_nodes = pd.read_csv("../midtstages/all_nodes.csv")
here_links = pd.read_csv('../midstages/all_links.csv')

# Filter1
here_links.FERRY_TYPE.unique()  #H - Not a Ferry, B - Boat Ferry, R-- Rail Ferry
print(len(all_links[all_links.FERRY_TYPE=='B'])) #102 ferry links, of which all are Bidirectional
all_links[all_links.FERRY_TYPE=='B']['DIR_TRAVEL'].unique()
# finding partner ids from PARTNER FILE
partner_ferry = partner_links[partner_links['LINK_ID'].isin(all_links[all_links.FERRY_TYPE=='B']['LINK_ID'])]
ferrylist1 = partner_ferry['LINK_ID'].to_list()
ferrylist2 = partner_ferry['partner_LINK_ID'].to_list()
ferrylist = ferrylist1 + ferrylist2
all_links_ca_noferry = all_links_ca_uni_length_f[~all_links_ca_uni_length_f['LINK_ID'].isin(ferrylist)]

#remove nodes associated with these links
ferry_links = all_links_ca_uni_length_f[all_links_ca_uni_length_f['LINK_ID'].isin(ferrylist)]
ferry_refnodes = ferry_links['REF_IN_ID'].to_list()
ferry_nrefnodes = ferry_links['NREF_IN_ID'].to_list()
ferrynodes = ferry_refnodes+ ferry_nrefnodes
print(len(ferrynodes))
ferrynodes_unique = set(ferrynodes)
len(set(ferrynodes_unique))
#checking weather these nodes are presnet in the rest. If present keep. ELse , remove - for CONNECTED GRAPH
ferrynodes_tokeep1 = all_links_ca_noferry[all_links_ca_noferry['REF_IN_ID'].isin(ferrynodes_unique)]['REF_IN_ID'].to_list()
ferrynodes_tokeep2 = all_links_ca_noferry[all_links_ca_noferry['NREF_IN_ID'].isin(ferrynodes_unique)]['NREF_IN_ID'].to_list()
ferrynodes_tokeep = ferrynodes_tokeep1 + ferrynodes_tokeep2
print(len(ferrynodes_tokeep))
ferrynodes_tokeep_unique = set(ferrynodes_tokeep)
print(len(ferrynodes_tokeep_unique))
# sorting both the lists
ferrynodes_tokeep1.sort()
ferrynodes_tokeep2.sort()
# using == to check if lists are equal
if ferrynodes_tokeep1 ==ferrynodes_tokeep2 :
    print ("The lists are identical")
else :
    print ("The lists are not identical")
# So there are 38 nodes out of all the 110 ferry nodes to keep . Remove the 72 nodes
ferry_nodes_remove = ferrynodes_unique - ferrynodes_tokeep_unique
len(ferry_nodes_remove)
all_nodes_noferry = all_nodes[~all_nodes['NODE_ID'].isin(ferry_nodes_remove)]

all_links_ca_noferry.to_csv("../midstages/all_links_noferry.csv", index = False)
all_nodes_noferry.to_csv("../midstages/all_nodes_noferry.csv", index = False)
