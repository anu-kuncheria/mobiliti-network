"""
Tasks
1.Filter out ferry links
"""
import pandas as pd

all_links_ca_uni_length_f = pd.read_csv('../data/midstages/all_links_ca.csv')
partner_links = pd.read_csv("../data/midstages/partner_link_ids.csv")
all_nodes = pd.read_csv("../midtstages/all_nodes.csv")
here_links = pd.read_csv('../data/midstages/all_links.csv')

# Filter1
print(here_links.FERRY_TYPE.unique())  #H - Not a Ferry, B - Boat Ferry, R-- Rail Ferry
print(len(all_links[all_links.FERRY_TYPE=='B'])) #102 ferry links, of which all are Bidirectional
print(all_links[all_links.FERRY_TYPE=='B']['DIR_TRAVEL'].unique())
# finding partner ids from PARTNER FILE
partner_ferry = partner_links[partner_links['LINK_ID'].isin(all_links[all_links.FERRY_TYPE=='B']['LINK_ID'])]
ferrylist1 = partner_ferry['LINK_ID'].to_list()
ferrylist2 = partner_ferry['partner_LINK_ID'].to_list()
ferrylist = ferrylist1 + ferrylist2
all_links_ca_noferry = all_links_ca_uni_length_f[~all_links_ca_uni_length_f['LINK_ID'].isin(ferrylist)]

#Remove nodes associated with the ferry links
ferry_links = all_links_ca_uni_length_f[all_links_ca_uni_length_f['LINK_ID'].isin(ferrylist)]
ferry_refnodes = ferry_links['REF_IN_ID'].to_list()
ferry_nrefnodes = ferry_links['NREF_IN_ID'].to_list()
ferrynodes = ferry_refnodes+ ferry_nrefnodes
print(len(ferrynodes))
ferrynodes_unique = set(ferrynodes)
print(len(set(ferrynodes_unique)))
#checking weather these nodes are presnet in the rest. If present keep. Else , remove - for connected graph structure
ferrynodes_tokeep1 = all_links_ca_noferry[all_links_ca_noferry['REF_IN_ID'].isin(ferrynodes_unique)]['REF_IN_ID'].to_list()
ferrynodes_tokeep2 = all_links_ca_noferry[all_links_ca_noferry['NREF_IN_ID'].isin(ferrynodes_unique)]['NREF_IN_ID'].to_list()
ferrynodes_tokeep = ferrynodes_tokeep1 + ferrynodes_tokeep2
ferrynodes_tokeep_unique = set(ferrynodes_tokeep)
ferrynodes_tokeep1.sort()
ferrynodes_tokeep2.sort()
# using == to check if lists are equal
if ferrynodes_tokeep1 ==ferrynodes_tokeep2 :
    print ("The lists are identical")
else :
    print ("The lists are not identical")

ferry_nodes_remove = ferrynodes_unique - ferrynodes_tokeep_unique
all_nodes_noferry = all_nodes[~all_nodes['NODE_ID'].isin(ferry_nodes_remove)]

all_links_ca_noferry.to_csv("../data/midstages/all_links_noferry.csv", index = False)
all_nodes_noferry.to_csv("../data/midstages/all_nodes_noferry.csv", index = False)
