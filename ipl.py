from functools import total_ordering

import numpy as np
import pandas as pd
import json
import ast

import campusx

class NpEncoder1(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder1, self).default(obj)


#initialized file path
ipl_matches = 'D:\Learning\DSMP 2.0\ipl-api-services\Datasets\IPL_Matches_2008_2022.csv'
ipl_matche_detail = 'D:\Learning\DSMP 2.0\ipl-api-services\Datasets\IPL_Ball_by_Ball_2008_2022.csv'
# 'https://drive.google.com/file/d/1R6O2oqQpIn3JSfFPjnq35XFPGhZXtbDg/view?usp=drive_link'

#read the CSV file
matches= pd.read_csv(ipl_matches)
matches_details=pd.read_csv(ipl_matche_detail)

matches['Team1Players'] = matches['Team1Players'].apply(ast.literal_eval)
ball_withmatch = matches_details.merge(matches, on='ID', how='inner').copy()
ball_withmatch['BowlingTeam'] = np.where(ball_withmatch['BattingTeam']==ball_withmatch['Team1'],ball_withmatch['Team2'],ball_withmatch['Team1'])
batter_data = ball_withmatch[np.append(matches_details.columns.values, ['BowlingTeam', 'Player_of_Match'])]


#function to get unique names of Team
def unique_teams_api():
    name = list(set(list(matches['Team1'].unique())+list(matches['Team2'].unique())))
    name_dict={'name':name}
    return name_dict

def unique_players():
    unique_players = matches.explode('Team1Players')['Team1Players'].unique()

    # # Convert to sorted list for better readability
    unique_players_list = sorted(unique_players)

    return {'players':unique_players_list}

def teams_record(team1,team2):
    total_matches = matches[((matches['Team1']==team1) & (matches['Team2']==team2) | (matches['Team1']==team2) & (matches['Team2']==team1))]
    total_matches_count=total_matches.shape[0]

    team1_winning=total_matches[total_matches['WinningTeam']==team1].shape[0]
    team2_winning = total_matches[total_matches['WinningTeam'] == team2].shape[0]

    # team2_winning=total_matches['WinningTeam'].value_counts()[team2]
    nr = total_matches[total_matches.WinningTeam.isnull()].shape[0]
    team1_loss=total_matches_count-team1_winning-nr


    return {
        'Total Matches Between Two Teams':total_matches_count,
        team1 + ' win':team1_winning,
        team2 + ' win':team2_winning,
        team1 + ' loss':total_matches_count - team2_winning,
        team2 + ' loss': total_matches_count - team1_winning
    }


def self_record(team):
    total_match = matches[matches['Team1'] == team].shape[0] + matches[matches['Team1'] == team].shape[0]
    total_win = matches[(matches['WinningTeam'] == team)].shape[0]
    total_loss = matches[((matches['Team1'] == team) | (matches['Team2'] == team)) & (matches['WinningTeam'] != team)].shape[0]
    title = matches[((matches['WinningTeam'] == team) & (matches['MatchNumber'] == 'Final'))].shape[0]

    return {
                    'matchesplayed':total_match,
                    'won':total_win,
                    'loss':total_loss,
                    'title':title
                   }
    # return team_record


def team_analysis(team,matches=matches):

    self_r=self_record(team)
    teams_unique=matches.Team1.unique()
    against={}
    for i in teams_unique:
        if team!=i:
            against[i] = teams_record(team,i)


    team_dict={team:{
                        'overall':self_r,
                        'against':against
                    }
               }
    return json.dumps(team_dict, cls=NpEncoder1)

def batsman_analysis(batsman_name,df):


    n1_detail = df[df['batter'] == batsman_name]

    out = n1_detail[n1_detail.player_out == batsman_name].shape[0]
    total_balls_played = n1_detail[n1_detail['extra_type'] != 'wide'].shape[0]

    total_match_played = n1_detail['ID'].unique().shape[0]
    total_run = n1_detail['batsman_run'].sum()
    total_fours = n1_detail[(n1_detail['batsman_run'] == 4) & (n1_detail['non_boundary'] == 0)].shape[0]
    total_six = n1_detail[(n1_detail['batsman_run'] == 6) & (n1_detail['non_boundary'] == 0)].shape[0]
    avg_run = total_run / out
    strike_rate = (total_run / total_balls_played) * 100
    total_fifties = n1_detail[n1_detail.groupby('ID')['batsman_run'].transform('sum') >= 50].ID.nunique()
    total_hundred = n1_detail[n1_detail.groupby('ID')['batsman_run'].transform('sum') >= 100].ID.nunique()
    highest_score = n1_detail.groupby('ID')['batsman_run'].sum().max()
    not_out = n1_detail[n1_detail.groupby('ID')['isWicketDelivery'].transform('sum') == 0].ID.nunique()
    mom = n1_detail[n1_detail['Player_of_Match'] == batsman_name].drop_duplicates('ID', keep='first').shape[0]

    data = {
        'total_matches_played':total_match_played,
        'total run':total_run,
        'total fours':total_fours,
        'total six':total_six,
        'avg run':avg_run,
        'strike rate':strike_rate,
        'total fifties':total_fifties,
        'total_hundred':total_hundred,
        'highest score':highest_score,
        'not out':not_out,
        'pom':mom
    }

    return data

def batsman_analysis_vs_team(batsman_name,teamname,df):

    df = df[df['BowlingTeam']==teamname].copy()
    return batsman_analysis(batsman_name, df)



def batsman_API(batsman_name,df=batter_data):
    df1 = df[df.innings.isin([1, 2])]
    individual = batsman_analysis(batsman_name,df=df1)

    teams_unique = matches.Team1.unique()
    against = {teamname:batsman_analysis_vs_team(batsman_name,teamname,df1) for teamname in teams_unique}

    # against = batsman_analysis_vs_team(batsman_name)
    final_data = {
                    batsman_name:
                        {
                            'all':individual,
                            'against':against
                    }
                  }
    return json.dumps(final_data,cls=NpEncoder1)