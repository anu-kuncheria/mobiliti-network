import pandas as pd

"""
Speeds for highways and ramps updated to match PeMS. Please refer to July 2021 updates in Documentation for more details.
"""

alllinks = pd.read_csv('../data/september2020/all_links.csv')
sub1 = alllinks[(alllinks['FUNC_CLASS'].isin([1,2])) & (alllinks['SPEED_KPH'].isin([80]))& (alllinks['CAPACITY(veh/hour)'] > 2000) & (alllinks['RAMP'] == 'N')]['LINK_ID'].values
sub2 = alllinks[(alllinks['FUNC_CLASS'].isin([1,2])) & (alllinks['SPEED_KPH'].isin([95]))& (alllinks['CAPACITY(veh/hour)'] > 2000) & (alllinks['RAMP'] == 'N')]['LINK_ID'].values
sub3 = alllinks[(alllinks['RAMP']=='Y') & (alllinks['SPEED_KPH'].isin([5,20,40]))]['LINK_ID'].values

alllinks_edited = alllinks.copy()
alllinks_edited['SPEED_KPH'] = np.where(alllinks_edited.LINK_ID.isin(sub1),95, alllinks_edited.SPEED_KPH)
alllinks_edited['SPEED_KPH'] = np.where(alllinks_edited.LINK_ID.isin(sub2),np.int(np.round(95*1.1)), alllinks_edited.SPEED_KPH)
alllinks_edited['SPEED_KPH'] = np.where(alllinks_edited.LINK_ID.isin(sub3),50, alllinks_edited.SPEED_KPH)
alllinks_edited.to_csv("../data/july2021/all_links.csv", index = False)


