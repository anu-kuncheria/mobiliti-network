import pandas as pd
import os

"""
Refer to July 2021 updates in Documentation for more details 
"""
def clip_areas(oldpath,alllinks_edited, cityname):
    old_links = pd.read_csv(oldpath)
    new_links = alllinks_edited[alllinks_edited['LINK_ID'].isin(old_links['LINK_ID'])]
    new_links.to_csv("{}_links.csv".format(cityname), index = False)


alllinks = pd.read_csv('../Nov2019/for_drive/september2020/all_links.csv')
sub1 = alllinks[(alllinks['FUNC_CLASS'].isin([1,2])) & (alllinks['SPEED_KPH'].isin([80]))& (alllinks['CAPACITY(veh/hour)'] > 2000) & (alllinks['RAMP'] == 'N')]['LINK_ID'].values
sub2 = alllinks[(alllinks['FUNC_CLASS'].isin([1,2])) & (alllinks['SPEED_KPH'].isin([95]))& (alllinks['CAPACITY(veh/hour)'] > 2000) & (alllinks['RAMP'] == 'N')]['LINK_ID'].values
sub3 = alllinks[(alllinks['RAMP']=='Y') & (alllinks['SPEED_KPH'].isin([5,20,40]))]['LINK_ID'].values
alllinks_edited = alllinks.copy()
alllinks_edited['SPEED_KPH'] = np.where(alllinks_edited.LINK_ID.isin(sub1),95, alllinks_edited.SPEED_KPH)
alllinks_edited['SPEED_KPH'] = np.where(alllinks_edited.LINK_ID.isin(sub2),np.int(np.round(95*1.1)), alllinks_edited.SPEED_KPH)
alllinks_edited['SPEED_KPH'] = np.where(alllinks_edited.LINK_ID.isin(sub3),50, alllinks_edited.SPEED_KPH)
alllinks_edited.to_csv("alllinks.csv", index = False)

clip_areas(sfoldpath,alllinks_edited, 'sf')
clip_areas(laoldpath,alllinks_edited, 'la')
