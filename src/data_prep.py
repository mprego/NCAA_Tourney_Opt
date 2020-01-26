import pandas as pd
import numpy as np

def create_round_results(seeds, rnd, teams, slots, res):
    '''
    Given a df of seeds, team info, slot information, and results, returns df of matchup and results
    '''
    seed_info = pd.merge(seeds, teams[['TeamID', 'TeamName']], on=['TeamID'], validate='m:1')
    
    # merge seed info with slots
    r_slots = slots.loc[slots['Round']==rnd]

    r_slot_seed = pd.merge(r_slots, seed_info,
                            left_on=['Season', 'StrongSeed'], right_on=['Season', 'Seed'], 
                            validate='1:1')
    r_slot_seed.drop('Seed', axis=1, inplace=True)

    r_slot_seed = pd.merge(r_slot_seed, seed_info, 
                            left_on=['Season', 'WeakSeed'], right_on=['Season', 'Seed'], 
                            validate='1:1', 
                            suffixes=['_Strong', '_Weak'])
    r_slot_seed.drop('Seed', axis=1, inplace=True)
    
    # add results
    r_results = pd.merge(r_slot_seed, res, 
                          left_on=['Season', 'Round', 'TeamID_Strong'], 
                          right_on=['Season', 'Round', 'TeamID'], 
                          validate='1:1')
    r_results.drop('TeamID', axis=1, inplace=True)

    r_results = pd.merge(r_results, res, 
                          left_on=['Season', 'Round', 'TeamID_Weak'], 
                          right_on=['Season', 'Round', 'TeamID'], 
                          validate='1:1', 
                          suffixes=['_Strong', '_Weak'])
    r_results.drop('TeamID', axis=1, inplace=True)


    r_results['TeamID_Winner'] = [w if ws>ss else s for w,s,ws,ss in 
                                   zip(r_results['TeamID_Weak'], r_results['TeamID_Strong'], 
                                       r_results['Score_Weak'], r_results['Score_Strong'])]
    return r_results