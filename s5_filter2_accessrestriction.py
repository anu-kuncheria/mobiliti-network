"""
Tasks
1.Access restrictions enable
"""
import pandas as pd

all_nodes_noferry = pd.read_csv("..\midstages\all_nodes_noferry.csv")
all_links_noferry = pd.read_csv("..\midstages\all_links_noferry.csv")
partner_links = pd.read_csv("..\midstages\partner_link_ids.csv")

def accessrest_filter_links(citylinks_df):
   #1. Thru links to include
    print("Length of all_links_noferry: ", len(all_links_noferry))
    thru_traff_yes = all_links[all_links['AR_TRAFF']=='Y']['LINK_ID'].to_list() #whole CA links to add from HERE
    print('Number of thru traffic links in original HeRE :',len(thru_traff_yes))
    thru_traff_ids = citylinks_df[citylinks_df['LINK_ID'].isin(thru_traff_yes)]['LINK_ID'].to_list() #all links to add
    print('Number of thru traffic links in all_links_noferry (not including my 7series):',len(thru_traff_ids))
    thru_traff_partners = partner_links[partner_links.LINK_ID.isin(thru_traff_ids)] #partners
    partner_city = thru_traff_partners['partner_LINK_ID'].to_list()
    thru_traff_city = set(thru_traff_ids+partner_city)
    print("Thru traffic links including my 7000 series is", len(thru_traff_city)) # 1. thru links with partners
    city_links_thru1 = citylinks_df[citylinks_df.LINK_ID.isin(thru_traff_city)]['LINK_ID'].to_list() #thru links to add
    print("Thru links for city to be included from all_links_noferry", len(city_links_thru1))

    #2. Selected nothru links to include
    thru_traff_no_df = all_links[all_links['AR_TRAFF']=='N'] #whole nothru links
    selected_thruno = thru_traff_no_df[(thru_traff_no_df['PUB_ACCESS']=='Y') & (thru_traff_no_df['AR_AUTO']=='Y') & (thru_traff_no_df['LOW_MBLTY']==2)]
    selected_thruno_links = selected_thruno['LINK_ID'].to_list() # to be selected
    selected_thruno_links_city = citylinks_df[citylinks_df['LINK_ID'].isin(selected_thruno_links)]['LINK_ID'].to_list()
    print('Number of selected no-thru traffic links (not including my 7series):',len(selected_thruno_links_city))
    selectednothru_partners = partner_links[partner_links.LINK_ID.isin(selected_thruno_links_city)]
    partner_city2 = selectednothru_partners['partner_LINK_ID'].to_list() #selected partner nothru
    nothruselected_total = selected_thruno_links_city+partner_city2 # selected no-thru links to include
    print('No-thru traffic links selected including my 7000 series is', len(nothruselected_total))

    #Final set of links
    fitered_links = set(city_links_thru1+nothruselected_total)
    print("Final set of links", len(fitered_links))
    filtered_df = citylinks_df[citylinks_df.LINK_ID.isin(fitered_links)]
    print("Final df", len(filtered_df))
    return filtered_df

def accessrest_filter_nodes(citynodes_df,citylinks_accessrest_df):
    print("length of all_nodes_noferry:", len(all_nodes_noferry))
    ref_nodes = citylinks_accessrest_df['REF_IN_ID'].to_list()
    nref_nodes = citylinks_accessrest_df['NREF_IN_ID'].to_list()
    nodes = set(ref_nodes+nref_nodes)
    print('Number of unique thru nodes nodes:', len(nodes))

    citynodes_filtered = citynodes_df[citynodes_df['NODE_ID'].isin(nodes)]
    print('Len of filtered nodes:', len(citynodes_filtered))
    return citynodes_filtered


all_links_noferry_thrufilter = accessrest_filter_links(all_links_noferry)
all_nodes_noferry_thrufilter  = accessrest_filter_nodes(all_nodes_noferry,all_links_noferry_thrufilter)
partner_links_thrufilter = partner_links[partner_links.LINK_ID.isin(all_links_noferry_thrufilter.LINK_ID)]

all_links_noferry_thrufilter.to_csv("../midstages/all_links_noferry_thrufilter.csv", index = False)
all_nodes_noferry_thrufilter.to_csv("../midstages/all_nodes_noferry_thrufilter.csv", index = False)
partner_links_thrufilter.to_csv("../midstages/partner_links_thrufilter.csv", index = False)
