import numpy as np
import pandas as pd
import json

#initialized file path
ipl_matches = 'D:\Learning\DSMP 2.0\ipl-api-services\Datasets\IPL_Matches_2008_2022.csv'
# 'https://drive.google.com/file/d/1R6O2oqQpIn3JSfFPjnq35XFPGhZXtbDg/view?usp=drive_link'

#read the CSV file
matches= pd.read_csv(ipl_matches)

#function to get unique names of Team
def unique_teams_api():
    name = list(set(list(matches['Team1'].unique())+list(matches['Team2'].unique())))
    name_dict={'name':name}
    return name_dict

def teams_record(team1,team2):
    total_matches = matches[((matches['Team1']==team1) & (matches['Team2']==team2) | (matches['Team1']==team2) & (matches['Team2']==team1))]
    total_matches_count=total_matches.shape[0]
    team1_winning=total_matches['WinningTeam'].value_counts()[team1]
    team2_winning=total_matches['WinningTeam'].value_counts()[team2]

    team_analysis={
        'Total Matches Between Two Teams':str(total_matches_count),
        team1:str(team1_winning),
        team2:str(team2_winning)
    }
    # print(team1_winning)
    return team_analysis

    # team1_total_win = matches[((matches['WinningTeam']==team1) & ((matches['Team1']==team2) | (matches['Team2']==team2)))].shape[0]
    # team2_total_win = matches[((matches['WinningTeam'] == team2) & ((matches['Team1'] == team1) | (matches['Team2'] == team1)))].shape[0]

    # return f'Total Matches Won By {team1} against {team2} is :', team1_total_win